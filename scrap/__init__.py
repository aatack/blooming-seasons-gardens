from utils.serialisation import deserialise_path as _deserialise
from scrap.base import Scrap as _Scrap
from os import listdir as _listdir


_SCRAP_PATH = "scrap"


for _file in _listdir(_SCRAP_PATH):
    if not _file.endswith(".py") or _file.startswith("__"):
        continue

    _loaded_module = _deserialise(_SCRAP_PATH + "." + _file.rstrip(".py"))

    for _attribute in dir(_loaded_module):
        _constructor = getattr(_loaded_module, _attribute)
        if isinstance(_constructor, type) and issubclass(_constructor, _Scrap):
            globals()[_attribute] = _constructor
