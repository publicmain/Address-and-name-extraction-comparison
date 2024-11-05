from name_util import find_closest_name,chinese_name_from_ocr,remove_title_prefix
from address_util import estimate_language_proportion,extract_address_id
from gpt import openai,openai_extract_name, openai_translate_to_english
from flask import Flask, request, jsonify,render_template
from process_util import output_from_ocr,is_idCard
from logging.handlers import RotatingFileHandler
from ocr_util import get_tenant_access_token
from decimal import Decimal, ROUND_HALF_UP
from config import app_id, app_secret
from similarity import compare_names
from difflib import SequenceMatcher
from serialNo import get_serialNo
import logging
import config
import json
import re



app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', backupCount=1, encoding='utf-8')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
filestream_logger = logging.getLogger('filestream_logger')
filestream_logger.setLevel(logging.INFO)
filestream_handler = RotatingFileHandler('filestream.log', backupCount=1, encoding='utf-8')
filestream_handler.setLevel(logging.INFO)
filestream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
filestream_handler.setFormatter(filestream_formatter)
filestream_logger.addHandler(filestream_handler)
@app.route('/')
def index():
    logger.info('Index page accessed')
    return render_template('index.html')

@app.route('/ocr/name_compare', methods=['POST'])
def extract_name():
    logger.info('--------------------------name_compare start--------------------------')
    data = request.json
    logger.info(f'request details for name_compare: {data}')
    if not data or 'name1' not in data or 'name2' not in data:
        logger.error('Missing parameters in /ocr/name_compare request')
        return jsonify({"error": "缺少必要参数: name1 或 name2"}), 400
    name1 = data['name1']
    name2 = data['name2']
    session_id = data.get('session_id', '')
    id_key = data.get('idKey', '')
    request_type = data.get('request', '')
    serialNo = get_serialNo()
    logger.info(f'Comparing names: {name1} and {name2}')
    # def contains_chinese(text):
    #     return re.search(r'[\u4e00-\u9fff]', text) is not None
    similarity = compare_names(name1,name2)
    similarity = Decimal(similarity)
    similarity = similarity.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    logger.info(f'Name comparison result: {similarity}%')
    return jsonify({
        "session_id": session_id,
        "idKey": id_key,
        "request": request_type,
        "name_result": str(similarity) + "%",
        "serialNo":serialNo,
        "real_address":"",
        "address_result":"",
        "output_name_from_URL":"",
        "real_name":"",
        "output_postal_from_URL":"",
        "output_address_from_URL":""
    }), 200

@app.route('/ocr/ocr_result', methods=['POST'])
def ocr_result():
    data = request.json
    if not data or 'filestream' not in data or "URL" not in data:
        logger.error('Missing parameters in /ocr/ocr_result request')
        return jsonify({"error": "缺少必要参数: file"}), 400

    filestream = data.get('filestream')
    URL = data.get('URL')
    session_id = data.get('session_id', '')
    id_key = data.get('idKey', '')
    request_type = data.get('request', '')
    access_token = get_tenant_access_token(app_id, app_secret)
    serialNo = get_serialNo()
    if not access_token:
        logger.error('Missing access_token in /ocr/ocr_result request')
        return jsonify({"error": "缺少access_token"}), 400
    if filestream == "":
        input_file = URL
    else:
        input_file = filestream
    try:
        output = output_from_ocr(input_file,access_token,True)
        logger.info(f'OCR result obtained from file: {output}')
    except Exception as e:
        logger.error("Failed to process file: %s", e)
        return jsonify({
            "error":str(e)
        }),500
    return jsonify({
        "serialNo":serialNo,
        "session_id": session_id,
        "idKey": id_key,
        "request": request_type,
        "ocr_output":output,
        "name_result": "",
        "real_address": "",
        "address_result":"",
        "output_name_from_URL":"",
        "real_name":"",
        "output_postal_from_URL":"",
        "output_address_from_URL":""
    }), 200

@app.route('/ocr/address_compare', methods=['POST'])
def address_compare():
    logger.info('--------------------------address_compare start--------------------------')
    data = request.json
    logger.info(f'request details for address_compare: {data}')
    if not data or 'address1' not in data or 'address2' not in data:
        logger.error('Missing parameters in /ocr/address_compare request')
        return jsonify({"error": "缺少必要参数: address1 或 address2"}), 400
    address1 = data['address1']
    address2 = data['address2']
    session_id = data.get('session_id', '')
    id_key = data.get('idKey', '')
    request_type = data.get('request', '')
    serialNo = get_serialNo()
    logger.info(f'Comparing addresss: {address1} and {address2}')
    # def contains_chinese(text):
    #     return re.search(r'[\u4e00-\u9fff]', text) is not None
    similarity = SequenceMatcher(None, address1, address2).ratio()
    similarity = Decimal(similarity)
    similarity = similarity.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    logger.info(f'address comparison result: {similarity}%')
    return jsonify({
        "session_id": session_id,
        "idKey": id_key,
        "request": request_type,
        "address_result": str(similarity) + "%",
        "serialNo":serialNo,
        "real_address":"",
        "output_name_from_URL":"",
        "real_name":"",
        "output_postal_from_URL":"",
        "output_address_from_URL":""
    }), 200

@app.route('/ocr/id_card_name_address', methods=['POST'])

def id_card_name_address():
    logger.info('--------------------------id_card_name_address extraction start--------------------------')
    data = request.json
    if not data or 'filestream' not in data or "URL" not in data:
        logger.error('Missing parameters in /ocr/id_card_name_address request')
        return jsonify({"error": "缺少必要参数: filestream or URL"}), 400

    filestream = data.get('filestream')
    URL = data.get('URL')
    session_id = data.get('session_id', '')
    id_key = data.get('idKey', '')
    request_type = data.get('request', '')
    access_token = get_tenant_access_token(app_id, app_secret)
    config.name = ''
    serialNo = get_serialNo()
    filestream_logger.info(f"\n\n\n\n\n---------------------------------=====================================---------------------------------\n\n\n\n\nfilestream for {session_id} is {filestream}")

    if not access_token:
        logger.error('Missing access_token in /ocr/id_card_name_address request')
        return jsonify({"error": "缺少access_token"}), 400
    if filestream == "":
        input_file = URL
    else:
        input_file = filestream
    try:
        
        output = output_from_ocr(input_file,access_token,True)
        # if is_chinese(output)
        logger.info(f"output from OCR: {output}")
        if is_idCard(output):
            output = output_from_ocr(input_file,access_token,False)   
            china_id = "Y"  
            extracted_name = chinese_name_from_ocr(output)
            extracted_address = extract_address_id(output)
            english_name = ""
            english_address = openai_translate_to_english(extracted_address) 
        else:
            china_id = "N"
            address_result = openai(output)
            logger.info(f'Address extraction result from OpenAI: {address_result}')
            serialNo = get_serialNo()
            parts = address_result.split("英文住址")
            logger.info(parts)
            if len(parts) == 2:
                extracted_address = parts[0].replace("原文住址：", "").replace("原文住址:", "").strip()
                english_address = parts[1].replace(":","").replace("：","").strip()
            else:
                extracted_address = ""
                english_address = ""
            name_result = openai_extract_name(output)
            logger.info(f'Name extraction result from OpenAI: {name_result}')
            name_data = json.loads(name_result)
            english_name = remove_title_prefix(name_data["英文姓名"])
            extracted_name = remove_title_prefix(name_data["原文姓名"])
        logger.info(f'ID card OCR result: Name - {extracted_name}, Address - {extracted_address}')
    except Exception as e:
        logger.error("Failed to process file: %s", e)
        return jsonify({
            "error":str(e)
        }),500
    return jsonify({
        "serialNo":serialNo,
        "session_id": session_id,
        "idKey": id_key,
        "china_id":china_id,
        "output_name_from_URL":extracted_name,
        "output_address_from_URL":extracted_address,
        "output_address_from_URL_en":english_address,
        "request": request_type,
        "real_address": "",
        "name_result":"",
        "real_name":english_name,
        "output_postal_from_URL":"",
        "address_result":""
    }), 200

@app.route('/ocr/ocrName_textName_compare', methods=['POST'])
def ocrName_textName_compare():
    data = request.json
    if not data or 'filestream' not in data or 'name' not in data or 'URL' not in data:
        logger.error('Missing parameters in /ocr/ocrName_textName_compare request')
        return jsonify({"error": "缺少必要参数: filestream or name"}), 400
    
    URL = data.get('URL')
    filestream = data.get('filestream')
    name = data['name']
    session_id = data.get('session_id', '')
    id_key = data.get('idKey', '')
    request_type = data.get('request', '')
    access_token = get_tenant_access_token(app_id, app_secret)
    serialNo = get_serialNo()
    config.name = name if name else ''
    if not access_token:
        logger.error('Missing access_token in /ocr/ocrName_textName_compare request')
        return jsonify({"error": "缺少access_token"}), 400
    if filestream == "":
        input_file = URL
    else:
        input_file = filestream
    try:
        output = output_from_ocr(input_file,access_token,True)
        value = estimate_language_proportion(output)
        if value > 0.5:
            
            if is_idCard(output):     
                extracted_name = chinese_name_from_ocr(output)
                similarity = compare_names(extracted_name,name)
            else:
                match, match_ratio = find_closest_name(name, output)
                similarity = match_ratio
                if match_ratio >= 70:
                    extracted_name = match
                else:
                    extracted_name = ""
                
        else:
            name_result = openai_extract_name(output)
            logger.info(f'Name extraction result from OpenAI: {name_result}')
            name_data = json.loads(name_result)
            original_name = name_data["原文姓名"]
            # _ , extracted_name = process_file(input_file, access_token)
            similarity = compare_names(original_name,name)
         
        logger.info(f'OCR name-text comparison result: {similarity}% similarity between {original_name} and {name}')
    except Exception as e:
        logger.error("Failed to process file: %s", e)
        return jsonify({
            "error":str(e)
        }),500
    
    return jsonify({
        "session_id": session_id,
        "idKey": id_key,
        "serialNo":serialNo,
        "request": request_type,
        "name_result":str(similarity) + "%",
        "output_name_from_URL":original_name,
        "real_address": "",
        "output_address_from_URL":"",
        "real_name":"",
        "output_postal_from_URL":"",
        "address_result":""
    }), 200


@app.route('/ocr/address_extract', methods=['POST'])
def address_name_ai_extract():
    data = request.json
    if not data or 'filestream' not in data or 'URL' not in data:
        logger.error('Missing parameters in /ocr/address_extract request')
        return jsonify({"error": "缺少必要参数"}), 400

    access_token = get_tenant_access_token(app_id, app_secret)
    if not access_token:
        logger.error('invalid access_token in /ocr/address_extract request')
        return jsonify({"error": "缺少access_token"}), 400
    filestream = data.get('filestream')
    URL = data.get('URL')
    session_id = data.get('session_id', '')
    id_key = data.get('idKey', '')
    request_type = data.get('request', '')
    try:
        if filestream == "":
            input_file = URL
        else:
            input_file = filestream
        # logger.info(f'Extracting address from file: {input_file}')
        output = output_from_ocr(input_file,access_token,True)
        address_result = openai(output)
        logger.info(f'Address extraction result from OpenAI: {address_result}')
        serialNo = get_serialNo()
        parts = address_result.split("英文住址")
        logger.info(parts)
        if len(parts) == 2:
            original_address = parts[0].replace("原文住址：", "").strip()
            english_address = parts[1].replace(":","").replace("：","").strip()
        else:
            original_address = ""
            english_address = ""
        pattern = r'singapore \d{6}'
        match = re.search(pattern, english_address, re.IGNORECASE)
        if match:
            singapore_postcode = match.group()
        else:
            singapore_postcode = ""
        
        name_result = openai_extract_name(output)
        logger.info(f'Name extraction result from OpenAI: {name_result}')
        name_data = json.loads(name_result)
        original_name = name_data["原文姓名"]
        english_name = name_data["英文姓名"]
    except Exception as e:
        logger.error("Failed to process file: %s", e)
        return jsonify({
            "error":str(e)
        }),500
    response = {
        "session_id": session_id,
        "idKey": id_key,
        "request": request_type,
        "serialNo":serialNo,
        "real_address":original_address,
        "output_address_from_URL":english_address,
        "output_postal_from_URL":singapore_postcode,
        "output_name_from_URL":english_name,
        "real_name":original_name,
        "address_result":"",
        "name_result": ""
    }

    return jsonify(response), 200

valid_keys = config.valid_keys
@app.route('/validate-key', methods=['POST'])
def validate_key():
    data = request.json
    key = data.get('key')
    if key in valid_keys:
        logger.info(f'Key validation successful for key: {key}')
        return jsonify({"status": "success", "message": "Key is valid."})
    else:
        logger.error(f'Invalid key: {key}')
        return jsonify({"status": "error", "message": "Key is invalid."}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18082, debug=False)

