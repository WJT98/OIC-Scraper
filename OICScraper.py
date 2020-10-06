import requests
from bs4 import BeautifulSoup
import re


ticker = "SPY"
def get_cnt():
	r = requests.get("https://www.optionseducation.org/toolsoptionquotes/optionsquotes")
	cnt = re.search("cnt=([A-F0-9]+)", r.text)
	return cnt.group().split("=")[1]
cnt = get_cnt()
url = "https://oic.ivolatility.com/oic_adv_options.j?cnt="+cnt+"&ticker="+ticker+"&exp_date=-1"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
print(list(soup.children))