# write to a file

with open("notes.txt","w") as file:
    file.write("learning python for genai.Which is important to study to study")

# read the file

# with open("notes.txt","r") as file:
#     content = file.read()

# print(content)

# with open("notes.txt","r") as file:
#     for line in file:
#         print(line)


import json
user={
    "name":"ritik",
    "skills":["python","java"],
    "experience":2
}
# python dict to json string
json_string = json.dumps(user)
print(type(json_string));

# json string --> python dictionay
data = json.loads(json_string)
print(type(data))