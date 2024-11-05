# import re
# from collections import Counter
# def calculate_letter_frequency(text):
#     return Counter(text)

# def compare_texts(text1, text2):
#     freq1 = calculate_letter_frequency(text1)
#     freq2 = calculate_letter_frequency(text2)
#     all_letters = set(freq1.keys()).union(set(freq2.keys()))
#     total_difference = 0
#     for letter in all_letters:
#         total_difference += abs(freq1.get(letter, 0) - freq2.get(letter, 0))
#     return total_difference

# def calculate_similarity(text1, text2):
#     text1 = re.sub(r'\d+', '', text1)
#     text2 = re.sub(r'\d+', '', text2)
#     total_difference = compare_texts(text1, text2)
#     max_length = max(len(text1), len(text2))
#     similarity_score = 1 - (total_difference / (2 * max_length))
#     return similarity_score