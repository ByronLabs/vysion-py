from vysion import client

API_KEY = "AIzaSyAzmeoGpzXJDxxIf8xEYSSKbOIqyMQYkLI"

c = client.Client(apiKey=API_KEY)

emails = c.find_email("purplefdw@protonmail.ch")
