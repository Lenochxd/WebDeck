def merge_dicts(d1, d2):
    """
    Merge two dictionaries taking including subdictionaries.
    Keys in d2 overwrite corresponding keys in d1, unless they are part of a subdictionary.
    """
    for key in d2:
        if key in d1 and isinstance(d1[key], dict) and isinstance(d2[key], dict):
            # Recursively, we merge the subdictionaries with the merge_dict method.
            merge_dicts(d1[key], d2[key])
        else:
            # If the key exists in d1 and it is not a subdictionary, we replace it with that of d2.
            d1[key] = d2[key]
    return d1