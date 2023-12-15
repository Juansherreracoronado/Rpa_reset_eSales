import os
import time
from ultralytics import YOLO
from IPython.display import display, Image
from roboflow import Roboflow
import subprocess

start_time = time.time()

rf = Roboflow(api_key="YOUR-API-KEY")
project = rf.workspace("cos10-85pn0").project("hik_labels")
dataset = project.version(1).download("yolov8")
model = YOLO('yolov8n.pt')
results = model.train(data=f'{dataset.location}/data.yaml', epochs=25, imgsz=800 ,plots=True)
Validate = model.val(model = r'C:\Users\admin\Documents\Rpa\runs\detect\train\weights\best.pt', data=f'{dataset.location}/data.yaml')


end_time = time.time()
runtime = end_time - start_time
print(f'Runtime in {runtime} seconds')