import unittest
import tempfile
from ..back_end.chunk_semantically import semantic_retriever 

class TestSemanticRetriever(unittest.TestCase):
    def setUp(self):
        # Replace 'file.txt' with the actual path to your test file
        test_file_path = 'file.txt'
        
        try:
            with open(test_file_path, 'r') as file:
                self.sample_content = file.read()
        except FileNotFoundError as e:
            self.fail(f"Test file not found: {test_file_path}. {e}")

        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(self.sample_content.encode())
        self.temp_file.close()

    def tearDown(self):
        # Delete the temporary file after testing
        import os
        os.unlink(self.temp_file.name)

    def test_semantic_retriever(self):
        result = semantic_retriever(self.temp_file.name)
        # Add your assertions based on the expected output
        self.assertTrue(isinstance(result, list))
        self.assertTrue(all(isinstance(chunk, str) for chunk in result))

if __name__ == '__main__':
    unittest.main()
