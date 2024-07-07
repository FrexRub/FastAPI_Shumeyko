ls = [
    {"a": 1, "b": 2},
    {"a": 10, "b": 20},
    {"a": 30, "b": 30},
    {"a": 40, "b": 40},
    {"a": 50, "b": 50},
]

ff = list(filter(lambda x: x["a"] == 1, ls))
print(ff)
