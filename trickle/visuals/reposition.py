from trickle.visuals.overlay import Overlay
from trickle.visuals.visual import Visual


class Reposition(Visual):
    def __init__(self, visual: Visual, x: float = 0.0, y: float = 0.0):
        self.visual = visual
        self.x = x
        self.y = y

    def simplify(self) -> "Visual":
        simplified_visual = self.visual.simplify()
        if isinstance(simplified_visual, Overlay):
            return Overlay(
                *(
                    Reposition(child.visual, x=self.x + child.x, y=self.y + child.y)
                    for child in simplified_visual.visuals
                )
            )
        else:
            raise Visual.invalid_simplified(simplified_visual)

    def width(self) -> float:
        return self.x + self.visual.width()

    def height(self) -> float:
        return self.y + self.visual.height()
