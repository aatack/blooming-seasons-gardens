from scrap.wrappers import Middleware
from scrap.base import defscrap, Scrap, rebuild
from scrap.composite import Group
from scrap.data import Point, Message
from scrap.control import Translate
from typing import List, Optional


@defscrap
class Reposition(Middleware):
    wrap: Scrap
    position: Point

    def inbound(self) -> Translate:
        return Translate(-self.position.x, -self.position.y)

    def outbound(self) -> Translate:
        return Translate(self.position.x, self.position.y)


@defscrap
class Column(Group):
    elements: List[Scrap]
    width: Optional[float] = None

    def children(self) -> List[Scrap]:
        children = []
        current_size = 0

        for element in self.elements:
            child = Reposition(element.Resize(width=self.width), Point(y=current_size))
            current_size += child.Bounds().message.height
            children.append(child)

        return children

    def _postprocessor(self, result: Scrap, event: Scrap) -> Scrap:
        modified_result = Group._DEFINITION.handlers.postprocessor(self, result, event)

        # TODO: make this more efficient - it currently rebuilds everything always
        return (
            rebuild(
                modified_result,
                scrap=rebuild(
                    self,
                    elements=[child.wrap for child in modified_result.scrap.children],
                ),
            )
            if isinstance(modified_result, Message)
            else rebuild(
                self, elements=[child.wrap for child in modified_result.children]
            )
        )


@defscrap
class Row(Group):
    elements: List[Scrap]
    height: Optional[float] = None

    def children(self) -> List[Scrap]:
        children = []
        current_size = 0

        for element in self.elements:
            child = Reposition(
                element.Resize(height=self.height), Point(x=current_size)
            )
            current_size += child.Bounds().message.width
            children.append(child)

        return children

    def _postprocessor(self, result: Scrap, event: Scrap) -> Scrap:
        modified_result = Group._DEFINITION.handlers.postprocessor(self, result, event)

        # TODO: make this more efficient - it currently rebuilds everything always
        return (
            rebuild(
                modified_result,
                scrap=rebuild(
                    self,
                    elements=[child.wrap for child in modified_result.scrap.children],
                ),
            )
            if isinstance(modified_result, Message)
            else rebuild(
                self, elements=[child.wrap for child in modified_result.children]
            )
        )
