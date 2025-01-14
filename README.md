# Address Verification & Similarity Check System

This project aims to **automate address verification** (e.g., for new credit card applications) by leveraging OCR (Feishu) and advanced text-matching algorithms. Users upload proof-of-address (bills, rental agreements, etc.) as images or PDFs; the system extracts text, computes **name/address similarity** against a target record, and outputs a score.

---

## Key Features

1. **OCR Extraction**  
   - Integrates **Feishu OCR** to recognize text from images/PDFs, supporting both Chinese and English.  
   - Automatically detects file format and chooses the appropriate processing flow.

2. **Name Similarity**  
   - Uses `difflib.SequenceMatcher` and `fuzzywuzzy` to compare English names.  
   - For Chinese names, converts them to Pinyin and applies fuzzy matching to enhance accuracy.

3. **Address Similarity**  
   - Leverages `SequenceMatcher` for English addresses and can handle mixed-lingual inputs via OpenAI-based translation.

4. **Rotation Detection & Face Cropping**  
   - Employs `dlib` to detect faces in ID cards. If detection fails, the image is rotated up to three times, maximizing OCR success rates.

5. **Monitoring & Auto-Restart**  
   - If the Flask process exits unexpectedly, a monitoring script automatically restarts the service and sends an alert email.  
   - Uses `RotatingFileHandler` to separate system logs and filestream logs for easier debugging.

---

## Tech Stack

- **Backend**: Python (Flask)  
- **OCR**: Feishu OCR, `PIL`, `opencv`, `dlib`  
- **Text Processing**: `fuzzywuzzy`, `difflib`, `pypinyin`, `re`  
- **AI & Translation**: OpenAI APIs  
- **Logging & Monitoring**: Python `logging` + `RotatingFileHandler` + custom auto-restart script  
- **Error Handling**: Exception capture, retry mechanisms, fallback strategies  

---

## Quick Start

1. **Install Dependencies**  
   - Requires Python 3.8+  
   - Clone or download this repository, then run:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configure OCR & OpenAI**  
   - In `config.py`, set `app_id` and `app_secret` for Feishu OCR.  
   - To enable translations via OpenAI, add your OpenAI Key in `gpt.py` (or use environment variables).

3. **Run the Application**  
   - Start the Flask server by running:
     ```bash
     python app.py
     ```
   - By default, it listens on `0.0.0.0:18082` (edit `app.py` if you need a different port).

4. **Monitoring & Auto-Restart (Optional)**  
   - To enable automatic restarts and email alerts, run:
     ```bash
     python monitor.py
     ```
   - Update email or SMTP settings in the script as needed.

---

## API Endpoints

1. **POST** `/ocr/ocr_result`  
   - **Purpose:** Extract text from a provided file stream (Base64) or a URL, leveraging OCR.  
   - **Params:**  
     - `filestream` (Base64-encoded file)  
     - `URL` (image or PDF link)  
   - **Response:** JSON containing OCR text or an error message.

2. **POST** `/ocr/name_compare`  
   - **Purpose:** Compare two names (English or Chinese) and return a similarity score.  
   - **Params:** `name1`, `name2`  
   - **Response:** Similarity in percentage.

3. **POST** `/ocr/address_compare`  
   - **Purpose:** Compare two addresses in English (or translated from Chinese) and return a similarity score.  
   - **Params:** `address1`, `address2`  
   - **Response:** Similarity in percentage.

4. **POST** `/ocr/id_card_name_address`  
   - **Purpose:** Specialized endpoint for ID cards, including facial detection and multiple rotations.  
   - **Params:** `filestream` or `URL`  
   - **Response:** Extracted name, address, and a flag indicating if it’s recognized as a Chinese ID.

5. **POST** `/ocr/address_extract`  
   - **Purpose:** AI-assisted extraction of both Chinese and English addresses, potentially with postal codes.  
   - **Params:** `filestream` or `URL`  
   - **Response:** Original address, translated address, possible postal code, etc.

---

## Challenges

- **Multi-Language Support:** Managing both English and Chinese name/address extraction.  
- **Variable OCR Quality:** Dealing with low-resolution images, poor lighting, or partial PDF scans.  
- **ID Card Rotation & Face Detection:** Using `dlib` to locate faces; if not found, rotating images up to three times.  
- **String Matching Accuracy:** Ensuring robust results across spelling variations, transliteration, and language mixing.  
- **Monitoring & Error Handling:** Preventing service downtime; swiftly restarting if needed and logging all exceptions in detail.

---

## Contributing

1. Fork the Repository and create a feature branch (e.g., `feature/your-feature`).  
2. Commit Your Changes with a clear message and reference any related issues.  
3. Open a Pull Request to the `main` branch. Your contribution will be reviewed and merged upon approval.

---

## License

This project is licensed under the [MIT License](./LICENSE). You are free to use, modify, and distribute under its terms.

---

## Contact

For questions or collaboration, feel free to reach me at `xxx@example.com`, or open an issue in this repository.

Thank you for your interest in this project!
