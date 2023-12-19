#from config import API_KEY
from vysion import client
import os

API_KEY = "DcFnTtBuQC4OIdtXy3VAY4LOlKcw162K1tfDA9wd"

c = client.Client(api_key=API_KEY)

result = c.search("madrid.org")
for hit in result.hits:
    print(hit.page.title)