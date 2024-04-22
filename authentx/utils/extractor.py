from typing import Dict, Any, Optional
from dataclasses import dataclass
import pdfplumber


@dataclass
class PDFFile:
    path: str
    text: Optional[str]
    metadata: Optional[Dict[str, Any]]

def extractor(file: PDFFile)-> str:
    with pdfplumber.open(file.path) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
    return text

if __name__ == "__main__":
    file = PDFFile(path="test/EEG_Text_Generation.pdf",
                   text=None, metadata=None)
    text = extractor(file)
    print(text)