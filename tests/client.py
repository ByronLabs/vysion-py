#from config import API_KEY
from vysion import client
import os
API_KEY = "YzhIAfsl9N8pFUurqq7lp6Nd25BCYwqf182sdNrF"
c = client.Client(api_key=API_KEY)
result = c.search("madrid.org")
#print results of result variable
print(result)
