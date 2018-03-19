

message = "hey ! /e-thumbs"

a = message.split("/")

for content in a:
    if content[0:2] == "e-":
        print(content[2:])
    else:
        print(content)
