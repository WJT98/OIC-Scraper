import requests
from bs4 import BeautifulSoup
import re
from datetime import date
import os
import errno
import numpy
import pandas as pd


ticker = "SPY"
def get_cnt():
	r = requests.get("https://www.optionseducation.org/toolsoptionquotes/optionsquotes")
	cnt = re.search("cnt=([A-F0-9]+)", r.text)
	return cnt.group().split("=")[1]

def get_html(ticker, date):
	cnt = get_cnt()
	url = "https://oic.ivolatility.com/oic_adv_options.j?cnt="+cnt+"&ticker="+ticker+"&exp_date=-1"
	print(url)
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	filename = os.path.join(os.getcwd(),ticker+"/"+date+".html")
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	with open(filename, "w", encoding='utf-8') as f:
		f.write(str(soup))

def store_data(ticker, date):
	with open("SPY"+"/"+date+".html", 'r', encoding='utf-8') as f:
		contents = f.read()
	soup = BeautifulSoup(contents, 'lxml')
	table = soup.find_all('table')
	df =[]
	expiry_dates = soup.find_all(text=re.compile("Expiry: [A-Za-z]{3} [0-9]{2}, [0-9]{4}"))
	for i in range(len(expiry_dates)):
		expiry_dates[i] = expiry_dates[i][0:20]
	print(expiry_dates)
	df.append(pd.DataFrame(expiry_dates))
	for i in range(1,len(table)):
		if len(table[i].find_all(text=re.compile("Gamma"))) > 0:
			df.append(pd.read_html(str(table[i]), flavor='bs4', header=[1])[0])
	return df

def main():
	today = date.today()
	d = today.strftime("%Y-%m-%d")
	filename = os.path.join(os.getcwd(),ticker+"/"+d+".html")
	if not os.path.exists(filename):
		get_html("SPY", d)
	df = store_data("SPY", d)
	col = list(df[-1].columns.values) 
	print(df[0].head())
	print(df[1].head())

	
main()