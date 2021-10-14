from scrap.base import defscrap, Scrap, rebuild
from scrap.composite import Wrapper
from typing import Any, List, Union


@defscrap
class Controller(Wrapper):
    """
    Passes a model to a view via a call to its View method.
    
    The scrap returned from that call is wrapped, and any messages it sends back are
    wrapped again.  If it sends through a message with a request to change the state of
    the model (see other scraps defined in this file), then that change will be made and
    the view will be rebuilt from the new model.
    """

    model: Scrap
    view: Scrap

    def wrap(self) -> Scrap:
        return self.view.View(self.model)

    def _postprocessor(self, result: Scrap, event: Scrap) -> Scrap:
        print(result, event)
        return Wrapper._DEFINITION.handlers.postprocessor(self, result, event)


@defscrap
class View:
    model: Scrap


@defscrap
class Update:
    path: List[Union[str, int]]
    value: Any
