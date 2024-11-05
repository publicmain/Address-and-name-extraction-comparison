from fuzzywuzzy import fuzz
import re
def find_closest_name(name, initial_text):
    max_ratio = 0
    closest_match = None

    for item in initial_text:
        ratio = fuzz.ratio(name.lower(), item.lower())
        if ratio > max_ratio:
            max_ratio = ratio
            closest_match = item

    return closest_match, max_ratio

def extract_name(data):
    combined_string = ''.join(data)
    
    combined_string = re.sub(r'[^\u4e00-\u9fff]', '', combined_string)
    print(combined_string)
    birth_index = combined_string.find('出生')
    if birth_index != -1:
        before_birth = combined_string[:birth_index]
        male_count = before_birth.count('男')
        female_count = before_birth.count('女')    
        if female_count == 1 and male_count == 0:
            before_birth = before_birth.replace('女', '', 1)
        elif female_count == 2 and male_count == 0:
            before_birth = before_birth.replace('女', '', 1)
        elif male_count == 1 and female_count == 0:
            before_birth = before_birth.replace('男', '', 1)
        elif male_count == 2 and female_count == 0:
            before_birth = before_birth.replace('男', '', 1)
        elif male_count == 1 and female_count == 1:
            first_male_index = before_birth.find('男')
            first_female_index = before_birth.find('女')
            if first_male_index < first_female_index:
                before_birth = before_birth[:first_female_index] + before_birth[first_female_index + 1:]
            else:
                before_birth = before_birth[:first_male_index] + before_birth[first_male_index + 1:]
        combined_string = before_birth + combined_string[birth_index:]
    combined_string = re.sub(r'[^\u4e00-\u9fa5]', '', combined_string)
    match = re.search(r'(.*?)性别', combined_string)
    if match:
        name_part = match.group(1)
        if '民族' in name_part:
            name_part = name_part.split('民族')[0]
        name_part = re.sub(r'姓名', '', name_part)
        return name_part.strip()
    return ""

def remove_title_prefix(name):
    title_pattern = re.compile(r'^(mr|mrs|dr|miss|ms|prof|sir|madam)\.?\s+', re.IGNORECASE)
    return title_pattern.sub('', name).strip()

# def extract_english_name(ocr_result, name_target):
#     english_name = ""
#     for i, text in enumerate(ocr_result):
#         if text == name_target and i >= 1:
#             english_name = ocr_result[i-1]    
#     return english_name


def chinese_name_from_ocr(initial_text):
    chinese_name = extract_name(initial_text)
    return chinese_name
