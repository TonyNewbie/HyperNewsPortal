import json


# write your code here
json_string = input()
python_object = json.loads(json_string)
print(type(python_object))
print(python_object)
