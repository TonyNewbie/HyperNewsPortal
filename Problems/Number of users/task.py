# write your code here
with open('users.json', 'r') as json_file:
    python_dict = json.load(json_file)
print(len(python_dict['users']))
