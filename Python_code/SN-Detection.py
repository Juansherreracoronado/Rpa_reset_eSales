import os
import time
from ultralytics import YOLO
import re
import subprocess
import json
import shutil

start = time.time()

folderpath = r'C:\Users\admin\Documents\UiPath\Rpa_Reset_eSales\eSales_Images'
barcode_folder_path = r'C:\Users\admin\Documents\Rpa\runs\detect\predict\crops\Barcode'
file_path = r'C:\Users\admin\Documents\UiPath\Rpa_Reset_eSales\Python_code\esales_Form_Data.txt'

#Cargar variables de entorno (APIs, claves... etc)

def run_barcode_reader(input_type, input_path):
    exe_path = r'C:\Users\admin\Documents\Rpa\Barcode\bin\BarcodeReaderCLI.exe'

    args = [exe_path, f'-type={input_type}', input_path]

    cp = subprocess.run(args, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output = cp.stdout
    error = cp.stderr

    if error != "":
        print("STDERR:\n" + error)
        print("RETURN CODE:", cp.returncode)
        return None  # Return None if there's an error

    # Parse the JSON output
    try:
        result = json.loads(output)
        barcode_text = result["sessions"][0]["barcodes"][0]["text"]
        return barcode_text
    except (json.JSONDecodeError, KeyError, IndexError):
        print("Error parsing JSON or extracting barcode text.")
        return None

# Obtener datos de ticket
with open(file_path, 'r') as file:
    content = file.read()
    pattern = re.compile(r'serial number: (\w{9})', re.DOTALL)
    matches = pattern.findall(content)
    if matches:
        for match in matches:
            serial_number = match
    pattern = re.compile(r'ticket\s*number:\s*(\d+)', re.DOTALL | re.IGNORECASE)
    matches = pattern.findall(content)
    if matches:
        for match in matches:
            ticket_number = match
            ticket_path = f'C:\\Users\\admin\\Documents\\RPA_Reset_Ticket_Files\\{ticket_number}'
    print(f'Serial: {serial_number}, Ticket: {ticket_number}')
    file.close()



model = YOLO(r'C:\Users\admin\Documents\Rpa\runs\detect\train\weights\best.pt')
for filename in os.listdir(folderpath):
    filepath = os.path.join(folderpath, filename)
    predictions = model.predict(conf=0.25, source=filepath, save_crop=True)
    file_object = open(r'C:\Users\admin\Documents\Rpa\Other\OCR.txt', "w")    
    for barcode in os.listdir(barcode_folder_path):
        input_type = 'code128'
        input_image_path = os.path.join(barcode_folder_path, barcode)
        barcode_text = run_barcode_reader(input_type, input_image_path)

        if barcode_text is not None:
            line = f"{barcode_text} \n"
            file_object.writelines(line)
            # add file to directory
            if not os.path.exists(ticket_path):
                os.makedirs(ticket_path)
            shutil.copy(input_image_path,ticket_path)
            shutil.copy(filepath, ticket_path)
        else:
            line = f"{barcode}: Failed to get barcode \n"
            file_object.writelines(line)
    file_object.close()
    file_object = open(r'C:\Users\admin\Documents\Rpa\Other\OCR.txt', "r")
    content = file_object.read()
    file_object.close()
    shutil.copy(r'C:\Users\admin\Documents\Rpa\Other\OCR.txt', ticket_path)
    print(content)
    if (serial_number in content):
        result_comparison = 1
    else:
        result_comparison = 0
    resultados = open(r'C:\Users\admin\Documents\UiPath\Rpa_Reset_eSales\Python_code\Results.txt', "w") 
    line = f"{result_comparison}"
    resultados.writelines(line)
    resultados.close()
    #os.remove(barcode_folder_path)

# delete folder C:\Users\admin\Documents\Rpa\runs\detect\predict
#os.remove(r'runs\detect\predict')


end = time.time()
runtime =  end - start
print(f'Runtime in {runtime} seconds')