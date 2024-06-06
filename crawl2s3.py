from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import s3fs
import boto3
"""crawling data from website"""
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
file_name1 = f'dw_{timestamp}.csv'
file_name2 = f'best_{timestamp}.csv'
# aws_access_key_id = 'AKIA2UC26TBOZGJC2OCA'
# aws_secret_access_key = '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'
bucket_name = 'airflowytbucket'
# Initialize Boto3 S3 client
s3_client = boto3.client(
    's3'
)

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
s3_client.put_object(Bucket=bucket_name, Key=file_name1,Body=data_text)
driver.quit()
"""write to csv"""

# Download the file from S3
data = s3_client.get_object(Bucket=bucket_name, Key=file_name1)
csv_content = data['Body'].read().decode('utf-8')

df = csv_content.split('\n')
df = pd.Series(df).drop(index=[0,1,4]).reset_index(drop=True)
df = df.tolist()

for i in range(len(df)):
    df[i] = df[i].replace('       ', ' NaN ')
df = pd.DataFrame([x.split() for x in df])
df.columns = [f"{col} ({unit})" for col, unit in zip(df.iloc[0], df.iloc[1])]
df = df.iloc[2:].copy()
df.to_csv(f's3://airflowytbucket/{file_name2}', index=False)
