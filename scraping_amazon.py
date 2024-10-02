from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
query=input("Enter the Item: ")
if not os.path.exists("data"):
    os.makedirs("data")
d={'title':[],'price':[],'link':[]}
filenum=0
for i in range(1,20):
    driver.get(f"https://www.amazon.in/s?k={query}&page={i}&crid=C8ZUAFER9TKG&sprefix=laptop%2Caps%2C734&ref=nb_sb_ss_pltr-xclick_2_6") #visits this website 
    elements = driver.find_elements(By.CLASS_NAME, "puis-card-container")
    # print(elements)
    print(f"{len(elements)} items found on page {i}")
    for element in elements:
        # print(element.text) 
        data = element.get_attribute("outerHTML")
        with open(f"data/{query}_{filenum}.html","w",encoding="utf-8") as file:
            file.write(data)
            soup = BeautifulSoup(data,'html.parser')
            t=soup.find("h2")
        if t:
            title=t.get_text().strip()
            l=t.find("a")
            if l:
                link="https://amazon.in/"+l['href']
            else:
                link="N/A"
        else:
            t="N/A"
            l="N/A"
        p=soup.find("span",attrs={"class":'a-price-whole'})
        if p:
            price=(p.get_text().strip())
        else:
            price="N/A"
        d['title'].append(title)
        d['price'].append(price)
        d['link'].append(link)
        # print(title,link,price)
        # print(soup.prettify())
        filenum+=1
    time.sleep(3)
driver.close()
df=pd.DataFrame(data=d)
csv_filename=f"data/{query}_products.csv"
df.to_csv(csv_filename,index=False)
print(f"Data has been saved to {csv_filename}")
