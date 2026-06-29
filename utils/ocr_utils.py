"""
utils/ocr_utils.py
AURA AI — OCR extraction for scanned / image-based PDFs.
Works on Windows, Linux, and macOS.
"""

import io
import platform
import os


def extract_text_from_scanned_pdf(pdf_file) -> str:
    """
    Run Tesseract OCR on every page of a scanned PDF.

    Args:
        pdf_file: Streamlit UploadedFile or file-like / bytes object.

    Returns:
        Extracted text string, or an error message if OCR is unavailable.
    """
    # Normalise to bytes
    if hasattr(pdf_file, "read"):
        raw = pdf_file.read()
        if hasattr(pdf_file, "seek"):
            pdf_file.seek(0)
    else:
        raw = bytes(pdf_file)

    try:
        from pdf2image import convert_from_bytes
        import pytesseract

        # ── Tesseract path (Windows only) ──────────────────
        if platform.system() == "Windows":
            candidates = [
                r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            ]
            for path in candidates:
                if os.path.isfile(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break

        # ── Poppler path (Windows only) ────────────────────
        poppler_kwargs: dict = {}
        if platform.system() == "Windows":
            win_poppler = [
                r"C:\Users\Administrator\Downloads\Release-23.08.0-0\poppler-23.08.0\Library\bin",
                r"C:\Program Files\poppler\bin",
                r"C:\poppler\bin",
            ]
            for p in win_poppler:
                if os.path.isdir(p):
                    poppler_kwargs["poppler_path"] = p
                    break

        images = convert_from_bytes(raw, dpi=200, **poppler_kwargs)
        pages: list[str] = []
        for img in images:
            pages.append(pytesseract.image_to_string(img))
        return "\n".join(pages)

    except ImportError:
        return (
            "OCR dependencies not installed.\n"
            "Run: pip install pdf2image pytesseract Pillow\n"
            "Also install Tesseract OCR from https://github.com/tesseract-ocr/tesseract\n"
            "and Poppler from https://poppler.freedesktop.org"
        )
    except Exception as exc:
        return f"OCR failed: {exc}"
