from vysion import client
import os

c = client.Client(api_key="In2BMeihwI3d1fGFsDoec4J4prBkrVReKYANH8Y3")
result = c.search_im("telegram", "madrid")

print(result)