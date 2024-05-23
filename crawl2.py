from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
"""crawling data from website"""
def selectdrop(nameele):
    WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, f"{nameele}"))
    )
    name_select = Select(driver.find_element(By.NAME, f"{nameele}"))
    name_select.first_selected_option

driver = webdriver.Firefox()
driver.get("http://weather.uwyo.edu/upperair/sounding.html")
driver.switch_to.frame(1)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "region"))
)
region = Select(driver.find_element(By.NAME, "region"))
region.select_by_value("seasia")

selectdrop("TYPE")
selectdrop("YEAR")
selectdrop("MONTH")
selectdrop("FROM")
selectdrop("TO")

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "STNM"))
)
station_select = driver.find_element(By.NAME, "STNM")
station_select.clear()
station_select.send_keys("48453")
station_select.send_keys(Keys.RETURN)

time.sleep(8)

"""change to new window and write list of unstuctured data"""

new_window = driver.window_handles
driver.switch_to.window(new_window[-1])
new = driver.current_url

response = requests.get(new)

soup = BeautifulSoup(response.content, 'html.parser')

pre_tag = soup.find("pre")
if pre_tag:
    data_text = pre_tag.text
with open("downloaded_data.csv", "w") as file:
    file.write(data_text)


"""using pandas to restructure data and save to csv file"""

df = pd.read_csv('downloaded_data.csv', header=None,skiprows=2).drop(index=[2]).reset_index(drop=True)
df = df.to_string(index=False).split('\n')

for i in range(len(df)):
    df[i] = df[i].replace('       ', ' NaN ')
df = df[1:]
df = pd.DataFrame([x.split() for x in df])
df.columns = [f"{col} ({unit})" for col, unit in zip(df.iloc[0], df.iloc[1])]
df = df.iloc[2:].copy()
df.to_csv('best.csv', index=False)
