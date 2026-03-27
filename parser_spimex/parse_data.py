import pdfplumber


def get_table(file_name: str):
    with pdfplumber.open(file_name) as pdf_file:
        for index, page in enumerate(pdf_file.pages):
            yield index, page.extract_table()
