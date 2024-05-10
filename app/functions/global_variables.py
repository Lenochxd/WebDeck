import json    


with open("data.json", encoding="utf-8") as f:
    data = json.load(f)
    
    if 'temp' not in data.keys():
        data['temp'] = {'vars': {}}
        
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)
        

def set_global_variable(variable_name, value):
    data['temp']['vars'][variable_name] = value
        
    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

def get_global_variable(variable_name):
    with open("data.json", encoding="utf-8") as f:
        data = json.load(f)
        
    if variable_name not in data['temp']['vars'].keys():
        return None
    
    return data['temp']['vars'][variable_name]