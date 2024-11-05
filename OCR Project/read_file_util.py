import requests
from PIL import Image
import base64
import io
import fitz
import logging
def download_image_from_url(url):
    
    response = requests.get(url)
    if response.status_code == 200:
        try:
            image = Image.open(io.BytesIO(response.content))
            return image
        except:
            raise Exception("Failed to identify image. The URL may not contain an image file.")
    else:
        raise Exception(f"Failed to download image from URL. Status code: {response.status_code}")
def get_base64_code(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return image_base64
        except:
            raise Exception("Failed to read text from URL.")
    else:
        raise Exception(f"Failed to download text from URL. Status code: {response.status_code}")
def get_file_type_from_base64(base64_string):
    file_data = base64.b64decode(base64_string)
    jpg_signature = b'\xff\xd8\xff'
    png_signature = b'\x89PNG\r\n\x1a\n'
    pdf_signature = b'%PDF'

    if file_data.startswith(jpg_signature):
        return 'jpg'
    elif file_data.startswith(png_signature):
        return 'png'
    elif file_data.startswith(pdf_signature):
        return 'pdf'
    else:
        return 'unknown'
def pdf_to_image(pdf_bytes):
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

def get_file_type_from_base64(base64_string):
    try:
        file_data = base64.b64decode(base64_string)
        jpg_signature = b'\xff\xd8\xff'
        png_signature = b'\x89PNG\r\n\x1a\n'
        pdf_signature = b'%PDF'
        
        if file_data.startswith(jpg_signature):
            return 'jpg'
        elif file_data.startswith(png_signature):
            return 'png'
        elif file_data.startswith(pdf_signature):
            return 'pdf'
        else:
            return 'unknown'
    except Exception as e:
        logging.error("Failed to determine file type: %s", e)
        return 'unknown'

def download_image_from_filestream(base64_string):
    try:
        file_type = get_file_type_from_base64(base64_string)
        image_data = base64.b64decode(base64_string)
        if file_type == 'jpg' or file_type == 'png':
            image = Image.open(io.BytesIO(image_data))
            return image
        elif file_type == 'pdf':
            return pdf_to_image(image_data)
        else:
            raise ValueError("Unsupported file type")
    except Exception as e:
        logging.error("Failed to download image from filestream: %s", e)
        raise

def pdf_to_image(pdf_bytes):
    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = pdf_document.load_page(0) 
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img
    except Exception as e:
        logging.error("Failed to convert PDF to image: %s", e)
        raise

def convert_image_to_jpeg(image):
    with io.BytesIO() as output:
        image.convert("RGB").save(output, format="JPEG")
        jpeg_image = Image.open(io.BytesIO(output.getvalue()))
    return jpeg_image

def download_pdf_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            pdf_bytes = io.BytesIO(response.content)
            return pdf_bytes
        except: 
            raise Exception("Failed to read PDF from URL.")
    else:
        raise Exception(f"Failed to download PDF from URL. Status code: {response.status_code}")
def download_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            text = response.text.lower()

            return text
        except:
            raise Exception("Failed to read text from URL.")
    else:
        raise Exception(f"Failed to download text from URL. Status code: {response.status_code}")