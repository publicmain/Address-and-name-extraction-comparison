import re
import logging
import pandas as pd
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
def process_string_and_update_excel(input_string):
    import pandas as pd
    df = pd.read_excel("省市县区.xlsx")
    all_regions = pd.concat([df['省'], df['地级市'], df['县区']]).dropna().unique()
    two_char_substrings = set()
    for region in all_regions:
        region = str(region)
        for i in range(len(region) - 1):
            two_char_substrings.add(region[i:i+2])
    id_position = input_string.find('公民身份号码')
    if id_position != -1:
        input_string = input_string[:id_position]
    for i in range(len(input_string) - 1):
        two_chars = input_string[i:i+2]
        if two_chars in two_char_substrings:
            return input_string[i:].strip()
    return input_string.strip()

def remove_id_number(input_list):
    combined_string = ''.join(input_list)
    id_re18 = re.compile(r'([1-6][1-9]|50)\d{4}(18|19|20)\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]')
    id_re15 = re.compile(r'([1-6][1-9]|50)\d{4}\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}')
    combined_string = id_re18.sub('', combined_string)
    combined_string = id_re15.sub('', combined_string)
    return combined_string

def extract_address_id(ocr_output_list):
    combined_string = remove_id_number(ocr_output_list)
    combined_string = process_string_and_update_excel(combined_string)
    combined_string = re.sub(r'住址|任址|住扯|任扯|址', '', combined_string)
    combined_string = re.sub(r'[^\u4e00-\u9fa5\d]', '', combined_string)
    if combined_string.find('出生') != 1 or combined_string.find('性别') != 1 or combined_string.find('姓名') != 1:
        print("combined_string12" + "    "+ combined_string)
        combined_string = extract_address_id_without_excel_pre_process(ocr_output_list)
        return combined_string
    if combined_string:
        return combined_string
    if combined_string == '':
        return ''
    
def extract_address_id_without_excel_pre_process(ocr_output_list):
    combined_string = ''.join(ocr_output_list)
    gender_idx = combined_string.find('性别')
    date_idx = combined_string.find('日', gender_idx)
    if date_idx != -1:
        combined_string = combined_string[date_idx+1:]          
        birth_idx = combined_string.find('出生')
        if (birth_idx != -1) and (birth_idx < combined_string.find('公民身份号码')):
            combined_string = combined_string[birth_idx+2:]     
        combined_string = re.sub(r'[^\u4e00-\u9fa5\d]', '', combined_string)
        id_position = combined_string.find('公民身份号码')
        if id_position != -1:
            combined_string = combined_string[:id_position]
        for i, char in enumerate(combined_string):
            if not char.isdigit():
                combined_string = combined_string[i:]
                break
        combined_string = re.sub(r'住址|任址|住扯|任扯|址', '', combined_string)
        combined_string = process_string(combined_string)
        combined_string = re.sub(r'住址|任址|住扯|任扯|址', '', combined_string)
        return combined_string.strip()
    
    return ""

def process_string(input_string):

    df = pd.read_excel("省市县区.xlsx")

    all_regions = pd.concat([df['省'], df['地级市'], df['县区']]).dropna().unique()


    prefix = input_string[:2]


    if any(region.startswith(prefix) for region in all_regions):
        return input_string  
    else:

        return input_string[2:]  

def estimate_language_proportion(text):
    if isinstance(text, list):
        text = ' '.join(text)
    cleaned_text = re.sub(r'[\s\d\W_]+', '', text)
    chinese_count = len(re.findall(r'[\u4e00-\u9fff]', cleaned_text))
    total_count = len(cleaned_text)
    if total_count == 0:
        return 0
    return chinese_count / total_count
# def is_address(text, street_names):
#     postcode_match = re.search(r'(S|s)?\[\d{6}\]', text) or re.search(r'\b\d{6}\b', text)
#     if postcode_match:
#         return True
#     unit_number_match = re.search(r'#\d{1,2}-\d{1,5}', text)
#     if unit_number_match:
#         return True
#     block_match = re.search(r'\b(block|BLK|blk)\b', text, re.IGNORECASE)
#     if block_match:
#         return True
#     possible_address_match = re.search(r'(\b\d+[A-Za-z]?\s+\w+|\b\w+\s+\d+[A-Za-z]?\b)', text)
#     if possible_address_match:
#         address_part = possible_address_match.group()
#         address_words = set(address_part.lower().split())
#         if address_words & set(map(str.lower, street_names)):
#             return True
#     return False
# def combine_address_lines(texts, street_names):
#     combined_addresses = []
#     temp_address = []
#     name_target = None

#     for text in texts:
#         if is_address(text, street_names):
#             temp_address.append(text)
#             postcode_match = re.search(r'\b\d{6}\b', text)
#             if postcode_match:
#                 postcode_index = text.index(postcode_match.group())
#                 if all(not char.isdigit() for char in text[:postcode_index]):
#                     full_address = " ".join(temp_address)
#                     cleaned_address = full_address[:full_address.index(postcode_match.group()) + 6]
#                     combined_addresses.append(cleaned_address)
#                     if name_target is None:
#                         name_target = temp_address[0]
#                     temp_address = []
#         elif temp_address:
#             combined_addresses.append(" ".join(temp_address))
#             if name_target is None:
#                 name_target = temp_address[0]
#             temp_address = []

#     if temp_address:
#         combined_addresses.append(" ".join(temp_address))
#         if name_target is None:
#             name_target = temp_address[0]
#     return combined_addresses, name_target


# def load_street_names(filepath):
#     street_names = set()
#     # with open(filepath, 'r') as file:
#     #     for line in file:
#     #         words = line.strip().lower().split()
#     #         street_names.update(word for word in words if re.match(r'^[a-zA-Z]+$', word) and len(word) > 1)
#     return street_names

