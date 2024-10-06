import json    


with open("temp.json", "a+", encoding="utf-8") as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError:
        data = {}
    
    if 'temp' not in data.keys():
        data['temp'] = {'vars': {}}
        
    with open("temp.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)
        

def set_global_variable(variable_name, value):
    global data
    data['temp']['vars'][variable_name] = value
        
    with open("temp.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

def get_global_variable(variable_name):
    global data
    
    with open("temp.json", encoding="utf-8") as f:
        data = json.load(f)
        
    if variable_name not in data['temp']['vars'].keys():
        return None
    
    return data['temp']['vars'][variable_name]


def get_global_variables(variables_names):
    """Get multiple global variables at once

    This function is used to load multiple global variables at once without having to reload the temp.json file multiple times.

    Keyword arguments:
    variables_names -- A tuple of variable names to retrieve
    Return: A tuple of variable values, with None for any variables that don't exist
    """

    with open("temp.json", encoding="utf-8") as f:
        data = json.load(f)

    variables = ()
    for variable_name in variables_names:
        if variable_name not in data["temp"]["vars"].keys():
            variables += (None,)
        else:
            variables += (data["temp"]["vars"][variable_name],)

    return variables
