"""
utils/pdf_utils.py
AURA AI — PDF text extraction
Uses pdfplumber (primary) with PyPDF2 as fallback.
"""

import io


def extract_pdf_text(pdf_file) -> str:
    """
    Extract plain text from a PDF.

    Args:
        pdf_file: Streamlit UploadedFile or any file-like / bytes object.

    Returns:
        Extracted text string (empty string on failure).
    """
    # Normalise to bytes so we can re-use after the first read
    if hasattr(pdf_file, "read"):
        raw = pdf_file.read()
        if hasattr(pdf_file, "seek"):
            pdf_file.seek(0)
    else:
        raw = bytes(pdf_file)

    # ── pdfplumber (best quality) ──────────────────────────
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            for page in pdf.pages:
                pt = page.extract_text()
                if pt:
                    text_parts.append(pt)
        text = "\n".join(text_parts)
        if text.strip():
            return text
    except Exception:
        pass

    # ── PyPDF2 fallback ────────────────────────────────────
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(raw))
        parts = []
        for page in reader.pages:
            pt = page.extract_text()
            if pt:
                parts.append(pt)
        return "\n".join(parts)
    except Exception:
        pass

    return ""


def get_pdf_page_count(pdf_file) -> int:
    """Return the number of pages in a PDF (0 on error)."""
    if hasattr(pdf_file, "read"):
        raw = pdf_file.read()
        if hasattr(pdf_file, "seek"):
            pdf_file.seek(0)
    else:
        raw = bytes(pdf_file)

    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            return len(pdf.pages)
    except Exception:
        pass

    try:
        import PyPDF2
        return len(PyPDF2.PdfReader(io.BytesIO(raw)).pages)
    except Exception:
        return 0
