# processing/document_processor.py

import os
from docx import Document
import PyPDF2

class DocumentProcessor:
    """Minimal class to process DOCX, PDF, and TXT files"""
    
    @staticmethod
    def load_document(file_path: str) -> str:
        """
        Load document based on file extension
        Returns: text content as string
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.docx':
            return DocumentProcessor._load_docx(file_path)
        elif file_ext == '.pdf':
            return DocumentProcessor._load_pdf(file_path)
        elif file_ext == '.txt':
            return DocumentProcessor._load_txt(file_path)
        else:
            raise ValueError(
                f"Unsupported file type: {file_ext}. Use .docx, .pdf, or .txt"
            )
    
    @staticmethod
    def _load_docx(file_path: str) -> str:
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    
    @staticmethod
    def _load_pdf(file_path: str) -> str:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text.strip()
    
    @staticmethod
    def _load_txt(file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()