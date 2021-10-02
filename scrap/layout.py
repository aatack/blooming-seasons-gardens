from scrap.wrappers import Middleware
from scrap.base import defscrap, Scrap
from scrap.data import Point
from scrap.control import Translate


@defscrap
class Reposition(Middleware):
    wrap: Scrap
    position: Point

    def inbound(self) -> Translate:
        return Translate(-self.position.x, -self.position.y)

    def outbound(self) -> Translate:
        return Translate(self.position.x, self.position.y)
