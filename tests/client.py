from vysion import client
from secrets import API_KEY

c = client.Client(apiKey=API_KEY)

result = c.find_email("purplefdw@protonmail.ch")
result = c.search("tijuana")

for hit in result.hits:
    print(hit.page.title)

    {
        "data": result.json(),
        "status": 200
    }
