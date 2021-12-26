from typing import Any as _Any

from trickle.environment import Environment
from trickle.trickles.indexed import Folded, Indexed, Mapped
from trickle.trickles.interaction import Keyboard, Mouse, Screen
from trickle.trickles.keyed import Keyed
from trickle.trickles.log import Log
from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Constant, Derived, Variable
from trickle.trickles.trickle import Trickle
from trickle.visuals.overlay import Overlay
from trickle.visuals.reposition import Reposition
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual
from trickle.window import Window


def puddle(value: _Any) -> Puddle:
    if isinstance(value, Puddle):
        return value
    else:
        return Variable(value)