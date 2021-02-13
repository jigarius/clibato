def dict_merge(dict1: dict, dict2: dict):
    """
    Create a dictionary where dict2 is merged into dict1.

    Example: dict_merge(defaults, values)

    :param dict1: A dictionary.
    :param dict2: A dictionary.
    :return: A deeply merged dictionary.
    """
    result = {**dict1}

    for key in dict2:
        if key in result:
            # Merge dictionaries.
            if isinstance(result[key], dict) and isinstance(dict2[key], dict):
                result[key] = dict_merge(result[key], dict2[key])
                continue

            # Do not overwrite with non-empty strings.
            if isinstance(dict2[key], str) and dict2[key] == '':
                continue

        result[key] = dict2[key]

    return result
