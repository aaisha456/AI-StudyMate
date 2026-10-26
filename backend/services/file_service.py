from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt"
}


def extract_text_from_file(file_path):
    """
    Extract text from a PDF, DOCX, or TXT file.

    Returns:
        str: Extracted text from the uploaded file.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. "
            "Please upload a PDF, DOCX, or TXT file."
        )

    # PDF
    if extension == ".pdf":
        return extract_pdf_text(path)

    # DOCX
    if extension == ".docx":
        return extract_docx_text(path)

    # TXT
    if extension == ".txt":
        return path.read_text(
            encoding="utf-8",
            errors="ignore"
        ).strip()

    return ""


def extract_pdf_text(path):
    """Extract text from a PDF file."""

    reader = PdfReader(str(path))

    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text_parts.append(page_text.strip())

    return "\n\n".join(text_parts).strip()


def extract_docx_text(path):
    """Extract text from a DOCX file."""

    document = Document(str(path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n\n".join(paragraphs).strip()