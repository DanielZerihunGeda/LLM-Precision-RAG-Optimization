import pytest
import sys
import os

# The parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from data.self_generate import read_pdf  # Update the import statement

def test_read_pdf():
    pdf_file_path = 'file.pdf'  # Replace with an actual PDF file path

    # Call the function and check if the result is not empty
    result = read_pdf(pdf_file_path)
    assert result.strip() != ""

# the rest test todo

if __name__ == "__main__":
    pytest.main()
