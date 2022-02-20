from typing import Union

from trickle.trickles.puddle import Puddle, puddle
from trickle.trickles.singular import Derived
from trickle.visuals.surface import Surface

from components.component import Anonymous


class Text(Anonymous):
    def __init__(
        self,
        text: Union[str, Puddle],
        size: int,
        font: str = "segoeuisemibold",
        padding: int = 0,
    ):
        super().__init__(
            lambda _: Derived(
                lambda v: Surface.text(str(v), size, font=font, padding=padding),
                puddle(text),
            )
        )
