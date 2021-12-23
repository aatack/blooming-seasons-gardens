from typing import Any as _Any

from trickle.trickles.indexed import Folded, Indexed, Mapped
from trickle.trickles.interaction import Keyboard, Mouse, Screen
from trickle.trickles.keyed import Keyed
from trickle.trickles.log import Log
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived, Variable
from trickle.trickles.trickle import Trickle


def puddle(value: _Any) -> Puddle:
    if isinstance(value, Puddle):
        return value
    else:
        return Variable(value)
