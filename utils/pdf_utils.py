import PyPDF2
from pdf2image import convert_from_bytes
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
def extract_text_from_scanned_pdf(pdf_file):

    text = ""

    images = convert_from_bytes(
        pdf_file.read(),
        poppler_path=r"C:\Users\Administrator\Downloads\Release-23.08.0-0\poppler-23.08.0\Library\bin"
    )

    for image in images:

        page_text = pytesseract.image_to_string(image)

        text += page_text + "\n"

    return text
def extract_pdf_text(pdf_file):

    text = ""

    try:

        reader = PyPDF2.PdfReader(pdf_file)

        for page in reader.pages:
            text += page.extract_text() or ""

    except:
        pass

    return text