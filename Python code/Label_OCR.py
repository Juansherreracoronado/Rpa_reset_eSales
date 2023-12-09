import cv2
import os
import base64
import requests
#from PIL import Image

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
api_key = 'K86811103388957'


# Importar Imagen
file_object = open(r'C:\Users\admin\Documents\Rpa\OCR.txt', "w")
umbral = 100
for filename in os.listdir('RPA_eSALES_Label'):
    filepath = os.path.join('RPA_eSALES_Label', filename)
    img = cv2.imread(filepath)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_umbral = cv2.threshold(img_gray, umbral, 255, cv2.THRESH_BINARY_INV) 
    cv2.imwrite(filepath, img_umbral)
    _, buffer = cv2.imencode(".png", img_umbral)
    img_base64 = base64.b64encode(buffer).decode("utf-8")
    api_url = 'https://api.ocr.space/parse/image'
    image_data = base64.b64decode(img_base64)
    # Create a file-like object from the bytes data
    image_file = {'filename': ('image.png', image_data, 'image/png')}
    # Define the API parameters
    payload = {
        'apikey': api_key,
        'language': 'eng',
    }
    # Send a POST request to OCR.space API
    response = requests.post(api_url, files=image_file, data=payload)
    # Check the response
    if response.status_code == 200:
        # API request successful
        result = response.json()
        # Check if 'ParsedResults' key exists in the response
        if 'ParsedResults' in result:
            # Access the OCR results
            parsed_text = result['ParsedResults'][0].get('ParsedText', 'No OCR results found.')
        else:
            print("No 'ParsedResults' key found in the response.")
    else:
        # API request failed
        print(f"Error {response.status_code}: {response.text}")
    line = [filename, '\n', '\n', 'Base64 String:', '\n', parsed_text, '\n', '\n']
    file_object.writelines(line)
file_object.close()