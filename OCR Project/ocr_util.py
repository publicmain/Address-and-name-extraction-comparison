import base64
from io import BytesIO
import requests
from rotate import process_single_image_base64
def recognize_text_with_lark(image, access_token):
    url = "https://open-sg.larksuite.com/open-apis/optical_char_recognition/v1/image/basic_recognize"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    buffered = BytesIO()
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    data = {"image": image_base64}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        if response_data["code"] == 0:
            return response_data["data"]["text_list"]
        else:
            print(f"Error: {response_data['msg']} (code: {response_data['code']})")
            return []
    else:
        print(f"HTTP 请求失败，状态码: {response.status_code}")
        return []
def recognize_text_with_lark_filestream(filestream, access_token):
    url = "https://open-sg.larksuite.com/open-apis/optical_char_recognition/v1/image/basic_recognize"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    filestream = process_single_image_base64(filestream)
    data = {"image": filestream}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        if response_data["code"] == 0:
            return response_data["data"]["text_list"]
        else:
            print(f"Error: {response_data['msg']} (code: {response_data['code']})")
            return []
    else:
        print(f"HTTP 请求失败，状态码: {response.status_code}")
        return []
def recognize_text_with_lark_filestream_general(filestream, access_token):
    url = "https://open-sg.larksuite.com/open-apis/optical_char_recognition/v1/image/basic_recognize"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {"image": filestream}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        if response_data["code"] == 0:
            return response_data["data"]["text_list"]
        else:
            print(f"Error: {response_data['msg']} (code: {response_data['code']})")
            return []
    else:
        print(f"HTTP 请求失败，状态码: {response.status_code}")
        return []
def get_tenant_access_token(app_id, app_secret):
    url = "https://open-sg.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 0:
            return data["tenant_access_token"]
        else:
            raise Exception(f"Error getting access token: {data['msg']}")
    else:
        raise Exception(f"HTTP request failed: {response.status_code}")