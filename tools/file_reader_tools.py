from langchain.tools import tool
from PyPDF2 import PdfReader

class FileReadTool:
    @tool("Read uploaded PDF")
    def read_pdf(file_path: str) -> str:
        """Reads text content from a PDF file."""
        reader = PdfReader(file_path);
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text