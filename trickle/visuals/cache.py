from trickle.trickles.puddle import Puddle
from trickle.trickles.singular import Derived
from trickle.visuals.surface import Surface
from trickle.visuals.visual import Visual


def cache(visual: Puddle[Visual], transparent: bool = False) -> Puddle[Visual]:
    """
    Cache a visual to a pygame surface.

    This will generally improve performance (if a visual is infrequently updated) at the
    cost of using slightly more memory.  It does not guarantee that the visual will
    remain unchanged as it will only render the parts of the component that are in the
    positive regions of each axis.  As such it is best suited for entire components that
    have already been resized to the desired format, and just need to be moved around.
    """

    def _cache(v: Visual) -> Visual:
        return Surface(v.render_from_scratch(transparent))

    return Derived(_cache, visual)
