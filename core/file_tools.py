from PIL import Image
from docx import Document
from reportlab.pdfgen import canvas
import os


def resize_image(input_path, output_path, size=(800, 800)):
    img = Image.open(input_path)
    img.thumbnail(size)
    img.save(output_path)
    return output_path


def docx_to_pdf(docx_path, pdf_path):
    doc = Document(docx_path)

    c = canvas.Canvas(pdf_path)
    y = 800

    for para in doc.paragraphs:
        c.drawString(50, y, para.text)
        y -= 20

    c.save()
    return pdf_path


def image_to_pdf(image_path, pdf_path):
    img = Image.open(image_path)
    img.convert('RGB').save(pdf_path)
    return pdf_path
