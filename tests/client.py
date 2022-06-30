from vysion import client
from config import API_KEY

c = client.Client(api_key=API_KEY)

def test_email(email="purplefdw@protonmail.ch"):
    result = c.find_email(email)
    # result = c.search("tijuana")

    for hit in result.hits:
        print(hit.page.title)
