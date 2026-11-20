records = [
    {"x1" : 0, "label": "car", "inside": False},
    {"x1" : 1, "label": "person", "inside": True},
]

for record in records:
    for key, value in record.items():
        print("{}: {}".format(key, value))