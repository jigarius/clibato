def ensure_shape(data: dict, shape: dict, parents=None) -> bool:
    """
    Checks keys in 'data' conform with the ones in 'shape'.

    An error is raised if:
      - data is missing a key that exists in shape.
      - data has a key that shape doesn't have.

    :param data: A dictionary.
    :param shape: A dictionary with the expected shape.
    :param parents: The parent key (for internal use).

    :except KeyError
    """
    parents = parents or []

    extra_keys = list(data.keys() - shape.keys())
    if extra_keys:
        extra_keys.sort()
        keys = map(lambda k: '.'.join([*parents, k]), extra_keys)
        keys = ', '.join(keys)
        raise KeyError(f'Config has illegal keys: {keys}')

    missing_keys = list(shape.keys() - data.keys())
    if missing_keys:
        missing_keys.sort()
        keys = map(lambda k: '.'.join([*parents, k]), missing_keys)
        keys = ', '.join(keys)
        raise KeyError(f'Config has missing keys: {keys}')

    for key in shape:
        if not isinstance(shape[key], dict):
            continue

        if len(shape[key]) == 0:
            continue

        if not isinstance(data[key], dict):
            key = '.'.join([*parents, key])
            raise KeyError(f'Config must have keyed-values: #{key}')

        ensure_shape(shape[key], data[key], [*parents, key])
