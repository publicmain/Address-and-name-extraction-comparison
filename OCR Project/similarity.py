from fuzzywuzzy import fuzz
from xpinyin import Pinyin
from pypinyin import pinyin, Style
from itertools import product
from collections import Counter
def is_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

# def chinese_to_pinyin(text):
#     return Pinyin().get_pinyin(text)

def compare_names(name1, name2):
    if name1  == "" or name2 == "":
        similarity = 0
        return similarity
    if is_chinese(name1) and is_chinese(name2):
        list1 = list(name1)
        list2 = list(name2)
        list1 = [char for char in list1 if char != " "]
        list2 = [char for char in list2 if char != " "]
        counter1 = Counter(list1)
        counter2 = Counter(list2)
        intersection = sum((counter1 & counter2).values())
        union = sum((counter1 | counter2).values())
        similarity_percentage = (intersection / union) * 100 if union != 0 else 0
        return similarity_percentage

    if is_chinese(name1):
        name1 = generate_pinyin_combinations(name1)
    similarity = compare_chinese_pingyin_algo(name1,name2)
    return similarity
    
def generate_pinyin_combinations(name):
    pinyin_combinations = pinyin(name, style=Style.NORMAL, heteronym=True)
    # all_pinyin_lists = [item for sublist in pinyin_combinations for item in sublist]
    all_combinations = list(product(*pinyin_combinations))
    all_pinyin_names = [' '.join(combo) for combo in all_combinations]
    return all_pinyin_names

def get_name_max_similarity(pingyin1,pingyin2):
    pingyin1 = pingyin1.strip().upper()
    pingyin2 = pingyin2.strip().upper()
    pingyin1list = pingyin1.split()
    pingyin2list = pingyin2.split()
    if len(pingyin2list) != 0:
        lastname1 = pingyin1list[0]
    else:
        return 0
    if len(pingyin2list) != 0:
        lastname2 = pingyin2list[0]
    else:
        return 0
    firstname1= ""
    if len(pingyin1list) >=1:
        for char in pingyin1list[1:]:
            firstname1 += char
    firstname2 = ""
    if len(pingyin2list) >=1:
        for char in pingyin2list[1:]:
            firstname2 += char
    name1 = firstname1 + lastname1
    name2 = firstname2 + lastname2
    name3 = lastname1 + firstname1
    name4 = lastname2 + firstname2
    result1 = fuzz.ratio(name1, name2)
    result2 = fuzz.ratio(name1, name4)
    result3 = fuzz.ratio(name3, name2)
    result4 = fuzz.ratio(name3, name4)
    result = max(result1,result2,result3,result4)
    return result

def compare_chinese_pingyin_algo(pingyin1, pingyin2):
    similarity = []
    if isinstance(pingyin1,list):
        for name in pingyin1:
            result = get_name_max_similarity(name,pingyin2) 
            similarity.append(result)
        return max(similarity)
    else:
        result = get_name_max_similarity(pingyin1,pingyin2)
        return result

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import SequenceMatcher

# Custom function to tokenize the address into components
def custom_tokenizer(address):
    return address.split(", ")

# Sample addresses
address1 = "Building 7, Unit 3, Rooshenuangfuliyangguangxiaoqu32312312ce"
address2 = "Building 7, Unit 2, Room 203, Nature Community, No. 6 Walnut Street, North Second Ring Road, Wuhua District, Kunming City, Yunnan Province"

# Check for a more sensitive string difference
similarity = SequenceMatcher(None, address1, address2).ratio()

