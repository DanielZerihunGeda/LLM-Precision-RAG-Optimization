"""
Read pdf data source for our data set and to run test on our model
source file is file.pdf it will be converted into txt to be chunked 
and vectorized for retrieval.

"""
import PyPDF2

def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()

    return text

def save_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text)


pdf_file_path = 'file.pdf'
output_text = read_pdf(pdf_file_path)


output_file_path = 'output_file.txt'
save_to_file(output_text, output_file_path)

print(f'Text saved to {output_file_path}')