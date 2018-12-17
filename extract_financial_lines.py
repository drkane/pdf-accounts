import re
import argparse
import pdfplumber

def get_finances(pdf):

    finance_regex = r'(.*)\s+(\(?\-?[\,0-9]+\)?)\s+(\(?\-?[\,0-9]+\)?)$'

    def process_match(match):
        match = {
            "text": match[0],
            "value1": match[1],
            "value2": match[2]
        }
        for i in ("value1", "value2"):
            match[i] = match[i].replace(",", "")
            if match[i][0] == "(" and match[i][-1] == ")":
                match[i] = match[i].replace("(", "-").replace(")", "")
            match[i] = float(match[i])
        return match

    finances = []
    for ps in pdf.pages:
        for l in ps.extract_text(y_tolerance=20).split('\n'):
            match = re.search(finance_regex, l)
            if match:
                m = process_match(match.groups())
                m['page'] = ps.page_number
                finances.append(m)

    return finances

def main():
    parser = argparse.ArgumentParser(description='Extract financial lines from a PDF document')
    parser.add_argument('infile', type=argparse.FileType('rb'))
    args = parser.parse_args()

    pdf = pdfplumber.load(args.infile)
    rows = get_finances(pdf)
    for r in rows:
        print(r)

if __name__ == "__main__":
    main()
