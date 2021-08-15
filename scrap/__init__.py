def _():
    from scrap.base import Registry, defscrap, Scrap, rebuild
    from utils.serialisation import deserialise_path as _deserialise
    from os import listdir as _listdir

    scrap_path = "scrap"
    for _file in _listdir(scrap_path):
        if not _file.endswith(".py") or _file.startswith("__"):
            continue

        _loaded_module = _deserialise(scrap_path + "." + _file.rstrip(".py"))

    return {
        "defscrap": defscrap,
        "Scrap": Scrap,
        "rebuild": rebuild,
        **Registry._CONSTRUCTOR_LOOKUP,
    }


for _key, _value in _().items():
    globals()[_key] = _value
