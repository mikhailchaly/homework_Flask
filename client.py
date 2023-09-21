import requests

# response = requests.post(
#     "http://127.0.0.1:5000/advert",
#     json={
#         "title": "title_5",
#         "description": "description_3",
#         "owner": "owner_5",
#     },
# )


# response = requests.get(
#     "http://127.0.0.1:5000/advert/3"
# )

# response = requests.post(
#     "http://127.0.0.1:5000/advert",
#     json={
#         "title": "title 1",
#         "description": "description 1",
#         "owner": "owner_1",
#     },
# )

# response = requests.post(
#     "http://127.0.0.1:5000/advert",
#     json={
#         "title": "title_2",
#         "description": "description_2",
#         "owner": "owner_2",
#     },
# )

# response = requests.get(
#     "http://127.0.0.1:5000/advert/3",
#
# )

# response = requests.patch(
#     "http://127.0.0.1:5000/advert/3",
#     json={
#         "title": "title_new",
#         "description": "new",
#         "owner": "owner_new",
#     },
# )

# response = requests.delete(
#     "http://127.0.0.1:5000/advert/1",
# )

response = requests.get(
    "http://127.0.0.1:5000/advert/2",
)

# response = requests.delete(
#     "http://127.0.0.1:5000/advert/3",
# )
#
# response = requests.get(
#     "http://127.0.0.1:5000/advert/3",
# )

print(response.status_code)
print(response.json())