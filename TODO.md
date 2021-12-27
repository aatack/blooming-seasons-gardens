# TODO

List of things that still need to be done in the project.

- Proper navigation for the planner
    - Up/down with scroll wheel
    - Left/right with shift scrolling
    - In/out with control scrolling
    - Click and drag navigation?
- Suite of buttons to add a new plant or bed
    - Attach the buttons to each container currently in the garden
- Collapsible widgets

## Rework

-   ~~Start with the core data structure and build everything up from there.~~
-   ~~Core data structure is a garden.
    For now it will just contain one element, but in the future it will have additional metadata added to it.~~
-   ~~Elements are currently either beds, flowers, labels, or arrows.~~
    -   ~~Beds are simply groups of other elements with an offset (position) that defaults to zero.~~
    -   ~~Flowers take a name, size, colour, and offset (to their centres).
        Other customisation options for things like border size can be added later on.~~
    -   ~~Labels take a label (as a string), font size, offset.~~
    -   ~~Arrows take a start and an end position.
        The idea is that later on these will be able to be attached to things like plants and labels.~~
-   ~~Nothing will have a view method yet.
    View methods shall be built out individually for each of the four elements, and for the basic UI components individually.
    The existing view framework will be used: ideally, any view object will simply be a state that returns a view.~~
    -   ~~This may at some point be refactored into classes.~~
-   ~~Structs will be removed and **everything** will be done in terms of keyed state objects.
    Subclasses can be made where appropriate.~~
-   ~~State objects will be renamed to trickle objects and put into a new package.~~
    -   ~~By default they will only fire and receive events.~~
    -   ~~Stateful trickle objects, known as puddles, will be a subclass of trickle objects and will contain the existing `value()` method.~~

## Features

-   ~~Allow the basic elements to be drawn.
    Each one will have two drawing modes:~~
    -   ~~**plan view**: a top-down view of the element as it will appear in the final plan.~~
    -   ~~**editor view**: a UI box that will appear on the left hand side of the screen, and allow minutiae to be edited in fine detail.~~

    ~~The plan view is likely to be the easier of the two, so we will start there, and initially will not have the elements respond to any user inputs.~~
-   Look into using pyglet for hardware acceleration (currently quite CPU-intensive).
-   Force components to only be instantiated once.
-   Collapsible editor panes.
-   Work out how to limit the bounds of scrollable components (this may require intercepting events sent between trickles).
-   Allow string values to be edited.
-   Background images.
-   Adding new beds, flowers, labels, and arrows.
-   Saving and loading.

## Notes

-   The current functions `horizontal_extent` and `vertical_extent` could be build into
    a `View` class, which is a subclass of `Puddle[Visual]` and also supplied `with` and
    `height` parameters (both of which are instances of `Puddle[float]`).
