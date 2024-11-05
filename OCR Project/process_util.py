from ocr_util import recognize_text_with_lark_filestream,recognize_text_with_lark_filestream_general
from read_file_util import get_base64_code
import logging
# street_names = load_street_names('address.txt')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# def is_singapore_address(initial_text):
#     contains_singapore = any("SINGAPORE" or "Singapore" or "singapore" in element for element in initial_text)
#     if contains_singapore:
#         return True
#     else:
#         return False
def is_idCard(initial_text):
    is_idCard = any("公民" in element or "身份" in element for element in initial_text)
    if is_idCard:
        return True
    else:
        return False
# def process_image(image, access_token):
#     try:
#         if image is None:
#             raise FileNotFoundError("指定的图像文件未找到")
    
#         initial_text = recognize_text_with_lark(image, access_token)
#         logger.info("Ocr Result before process text")
#         if estimate_language_proportion(' '.join(initial_text)) < 0.5:
#             cropped_img = crop_image(image)
#             ocr_result = recognize_text_with_lark(cropped_img,access_token)
#             logger.info(ocr_result)
#             return process_english_text(ocr_result)
#         else:
#             ocr_result = recognize_text_with_lark(image,access_token)
#             logger.info(ocr_result)
#             return process_non_english_text(ocr_result)
#     except Exception as e:
#         logging.error("cannot fine image file: %s", e)
#         raise

# def process_english_text(initial_text):
#     relevant_ocr_result = find_relevant_ocr_result(initial_text)
    
#     cleaned_addresses, name_target = combine_address_lines(relevant_ocr_result, street_names)
#     english_name = extract_english_name(initial_text, name_target)
#     cleaned_address = ' '.join(cleaned_addresses)
    
#     return cleaned_address, english_name if english_name else ""

# def process_non_english_text(ocr_result):
#     chinese_name = extract_name(ocr_result)
#     ocr_text = ''.join(ocr_result)
#     cleaned_address = extract_address_and_id(ocr_text)
    
#     return cleaned_address, chinese_name

# def crop_image(image):
#     w, h = image.size
#     return image.crop((0, 0, w // 2, h // 2))

# def find_relevant_ocr_result(ocr_result):
#     relevant_ocr_result = []
#     for i, text in enumerate(ocr_result):
#         if compare_names(config.name, text) > 70:
#             relevant_ocr_result = ocr_result[i+1:]
#             break
#     if not relevant_ocr_result:
#         relevant_ocr_result = ocr_result
    
#     return relevant_ocr_result


    
def output_from_ocr(input_string,access_token,choose):
    # print(input_string)
    if choose == True:
        try:
            if input_string.startswith('https://') or input_string.startswith('http://'):
                image_base64 = get_base64_code(input_string)
                initial_text = recognize_text_with_lark_filestream_general(image_base64,access_token)  
            else:
                initial_text = recognize_text_with_lark_filestream_general(input_string, access_token)
            
            return initial_text
        except Exception as e:
            logging.error("Failed to download image from filestream: %s", e)
            raise
    else:
        try:
            if input_string.startswith('https://') or input_string.startswith('http://'):
                image_base64 = get_base64_code(input_string)
                initial_text = recognize_text_with_lark_filestream(image_base64,access_token)  
            else:
                initial_text = recognize_text_with_lark_filestream(input_string, access_token)
            
            return initial_text
        except Exception as e:
            logging.error("Failed to download image from filestream: %s", e)
            raise


# def process_file(input_string, access_token):
#     logger.info("Enter Non-ID process")
#     try:
#         if input_string.startswith('https://') or input_string.startswith('http://'):
#             if input_string.lower().endswith("pdf"):
#                 pdf_bytes = download_pdf_from_url(input_string)
#                 return process_pdf(pdf_bytes, access_token)
#             else:
#                 image = download_image_from_url(input_string)
#         else:
#             image = download_image_from_filestream(input_string)
#         return process_image(image, access_token)
#     except Exception as e:
#         logging.error("Failed to process file: %s", e)
#         raise

# def process_pdf(file, access_token):
#     pdf_bytes = file.read()
#     images = pdf_to_image(pdf_bytes)

#     if images:
#         return process_image(images, access_token)
