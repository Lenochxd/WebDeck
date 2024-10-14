global_vars = {}

def set_global_variable(variable_name, value):
    global global_vars
    global_vars[variable_name] = value

def get_global_variable(variable_name):
    global global_vars
    return global_vars.get(variable_name, None)

def get_global_variables(variables_names):
    """Get multiple global variables at once

    This function is used to load multiple global variables at once without having to reload the temp.json file multiple times.

    Keyword arguments:
    variables_names -- A tuple of variable names to retrieve
    Return: A tuple of variable values, with None for any variables that don't exist
    """
    global global_vars
    return tuple(global_vars.get(name, None) for name in variables_names)
