records = [
    {"x1" : 0, "label": "car", "inside": False},
    {"x1" : 1, "label": "person", "inside": True},
    {"x1" : 2, "label": "person", "inside": True},
    {"x1" : 3, "label": "person", "inside": True},
]

count = 0

for record in records:
    if record["inside"]:
        count += 1

print("구역 안: ", count)