import json  # For reading JSON annotation files
file_path = 'C:/Users/PC/Desktop/unfinish_project/prepare_dataset/footballs/football_test/Match_1864_1_0_subclip/Match_1864_1_0_subclip.json'

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)
            # Check data type
    print(data.keys()) 

# Ensure 'annotations' key exists
# Ensure 'annotations' key exists
# if "annotations" in data:
#     for index, ann in enumerate(data["annotations"]):
#         if ann.get("image_id") == 100 and ann.get("category_id") == 4:
#             print(f"Found at index {index} in 'annotations' list")
#             print(json.dumps(ann, indent=4))  # Pretty print the matching annotation
# else:
#     print("No 'annotations' key found in the JSON file.")
    # if not isinstance(data, list):
    #     raise TypeError(f"Expected data to be a list, but got {type(data).__name__}. Check JSON formatting.")

annotations = data["annotations"]
players = [anno for anno in annotations if anno.get("image_id") == 100 and anno.get("category_id") == 4]

print(len(players))

player = players[8]
jersey_number = player.get("attributes").get("jersey_number")
print(jersey_number)

xmin, ymin, w, h = player.get("bbox")
print(xmin, ymin, w, h)