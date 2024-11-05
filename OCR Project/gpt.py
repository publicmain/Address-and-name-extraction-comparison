from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
MODEL = "gpt-4o"
load_dotenv()
print(os.getenv("OCR_API_KEY"))
client = OpenAI(api_key=os.getenv("OCR_API_KEY"),)
name_query = "6K+G5Yir5paH5pys5L+h5oGv77yae3RleHR977yM5om+5Ye65paH5pys6YeM6Z2i5YyF5ZCr55qE5aeT5ZCN5piv5LuA5LmILO+8iOWPquaJvuWHuueUqOaIt+Wnk+WQje+8jOS4jeimgeaJvuWHuuWFtuS7lu+8ie+8jOW5tuS4lOe/u+ivkeaIkOiLseaWhywg6K+35rOo5oSP77yM5L2g55qE5Zue562U5LiA5a6a6KaB5Lil5qC85oyJ54Wn5qC85byP5bm26IO96KKr5q2j5bi46L2s5oiQanNvbuagvOW8j++8jOS4jeimgeW4puaciWpzb27ov5nkuKrlh6DkuKrlrZfnrKYge3si5Y6f5paH5aeT5ZCNIjoiIiwgIuiLseaWh+Wnk+WQjSI6IiJ9fe+8jOazqOaEj++8jOWmguaenOaWh+acrOmHjOeahOaYr+S4reaWh+WQjeWtl++8jOmCo+S5iOWwseS4jemcgOimgee/u+ivkeaIkOiLseaWh++8jOWOn+WFiGpzb27ph4zpnaLnmoTigJzoi7Hmloflp5PlkI3igJ3lrZfmrrXph4zpnaLloavlhaXkuK3mloflp5PlkI3ljbPlj68="

translate_query = "output only the translated text from {text} in english"


def base64_decode_file(input_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        encoded_data = file.read()
    decoded_data = base64.b64decode(encoded_data.encode('utf-8')).decode('utf-8')
    print(decoded_data)
    return decoded_data

def base64_decode_string(input):
    decoded_data = base64.b64decode(input.encode("utf-8")).decode('utf-8')
    print(decoded_data)
    return decoded_data

def openai(text):
    def read_from_txt(filename):
        content = base64_decode_file(filename)
        return content
    user_content_template = read_from_txt("query.txt")
    user_content = user_content_template.format(text=text)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": "you are my very helpful agent to extract the address from file"
            },
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": user_content}
                ]
            }
        ],
        temperature=0.0,
    )
    response_text = response.choices[0].message.content
    return response_text

def openai_extract_name(text):
    user_content_template = base64_decode_string(name_query)
    user_content = user_content_template.format(text=text)
    # print(user_content)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": "you are my very helpful agent to extract the name from file"
            },
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": user_content}
                ]
            }
        ],
        temperature=0.0,
    )
    response_text = response.choices[0].message.content
    # print(response_text)
    return response_text
# base64_decode_string(name_query)
# openai_extract_name("name: geihg    zabag agaeg aegaeg ahaehg a")


def openai_translate_to_english(text):
    user_content = translate_query.format(text=text)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": "you are my very helpful agent to translate from text"
            },
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": user_content}
                ]
            }
        ],
        temperature=0.0,
    )
    response_text = response.choices[0].message.content
    # print(response_text)
    return response_text