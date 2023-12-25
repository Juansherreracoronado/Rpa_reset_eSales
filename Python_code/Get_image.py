import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time
driver = webdriver.Chrome()
driver.get("https://hikvision.my.xiaoshouyi.com/customize_detail.action?id=3090081564445283&belongId=455")
time.sleep(3)
results = []
content = driver.page_source
soup = BeautifulSoup(content)
# funcion para encontrar las imagenes con beautifulsoup

def parse_image_urls(classes, location, source):
    for a in soup.findAll(attrs={"class": classes}):
        name = a.find(location)
        if name not in results:
            results.append(name.get(source))


parse_image_urls("s-item__image-wrapper image-treatment", "img", "src")
df = pd.DataFrame({"links": results})
df.to_csv("links.csv", index=False, encoding="utf-8")