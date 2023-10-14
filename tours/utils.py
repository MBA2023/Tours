def get_map_from_list(list_, exctract_key_func, extract_value_func=lambda elem: elem):
    result = {}
    for elem in list_:
        key = exctract_key_func(elem)
        result[key] = result.get(key, []) + [extract_value_func(elem)]
    return result
