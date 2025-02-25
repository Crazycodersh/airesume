import PyPDF2
import docx
import io
from typing import List, Dict, Union
from pathlib import Path

class DocumentProcessor:
    @staticmethod
    def extract_text(file) -> str:
        """Extract text from uploaded document file."""
        try:
            # Get file extension
            filename = file.name.lower()
            
            if filename.endswith('.pdf'):
                return DocumentProcessor._extract_from_pdf(file)
            elif filename.endswith('.docx'):
                return DocumentProcessor._extract_from_docx(file)
            else:
                raise ValueError(f"Unsupported file format: {Path(filename).suffix}")
                
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")

    @staticmethod
    def _extract_from_pdf(file) -> str:
        """Extract text from PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text.strip()
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    @staticmethod
    def _extract_from_docx(file) -> str:
        """Extract text from DOCX file."""
        try:
            doc = docx.Document(file)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text).strip()
        except Exception as e:
            raise Exception(f"Error processing DOCX: {str(e)}")

    @staticmethod
    def get_document_stats(text: str) -> Dict:
        """Calculate basic document statistics."""
        words = text.split()
        sentences = text.split('.')
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'char_count': len(text)
        }
