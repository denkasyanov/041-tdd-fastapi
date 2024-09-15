import pytest


def dict_parametrize(data, **kwargs):
    args = list(list(data.values())[0].keys())
    formatted_data = [[item[a] for a in args] for item in data.values()]
    ids = list(data.keys())
    return pytest.mark.parametrize(args, formatted_data, ids=ids, **kwargs)
