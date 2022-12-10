# Blooming Seasons Design Studio

## Setup

From this folder, run `npm install`.

## Development

To start the development server, run:

```bash
npm start
```

This should open a browser window running the app.
To access the electron interface, run:

```bash
npm run electron-dev
```

which opens an electron window running the local host address on which the app is running.
Changes to the source code should update that display live (upon saving).

## References

The initial project setup was done by following [a guide](https://medium.com/folkdevelopers/the-ultimate-guide-to-electron-with-react-8df8d73f4c97) and then removing all the boilerplate that wasn't strictly necessary.

## Feature requests

- [x] `from black import main`
- [x] Bed -> edit -> says "edit plant"
- [x] Can only load PNG
- [x] Popups appear on the wrong screen
- [x] Make a copy of a plant for bulk creation
  - Actually applies to any element
- [x] Plant sizes need to refer to their diameters
- [x] Better colour picker
- [x] Import images for plants
  - [x] Work out why the tickbox isn't picking up the right initial value
- [x] See the colour of a plant when picking it
- [x] Open the existing garden at a default location
  - This does sort of already happen, since the currently opened garden is part of the data structure that gets saved to local storage
  - Once saving is done every minute, this should be fine
- [x] Automatically save every minute
- [x] Thinner outline for plants and editable
- [x] Increase popup size
- [x] Plants should derive properties from the nursery always
- [x] Text bigger in the editor
  - Probably sufficient to just zoom in, though added something to the default CSS anyway
- [x] Display plant sizes alongside coordinates
- [x] Select and move with the arrow keys
- [x] Movement sensitivity changes with zoom level
- [x] Nursery terminology: template and instance
- [x] Make whole plant light up blue
- [x] **Undo**
- [x] Show plant preview in the list of plants in the nursery
- [x] Sort plants within a bed by name, and then by x-coordinate
- [x] Make editor width draggable
- [x] Make text font selectable
  - [x] Spectral
  - [x] Arial
- [x] Make open nursery for labels
  - [ ] Or, alternatively, click on a button to make a label for an existing plant
  - [ ] Presumably it would also be useful to be able to attach arrows to things, or at least make their start and end positions relative (eg. start is one unit below a particular plant)
- [x] Highlight everything in a bed when mousing over its collapsible area
- [x] Reverse highlighting: light up in editor when moused over in plan
- [x] Line breaks in labels
- [x] Centralise labels
- [x] Ability to add rectangles
- [ ] Checkbox that enables beds to be hidden temporarily
- [x] Hotkey for hiding the editor
  - Went with space in the end (keycode 32)
- [ ] Tabs: mood board, garden
- [ ] Snap to centre

### Others

- [ ] Make sure the plant's outer rendered radius (ie. including stroke width) matches its given radius when not using an icon
  - [ ] Also when the stroke thickness increases as it's hovered
- [ ] Invert the truthiness of the tickbox for selecting the template to use
  - [ ] Better yet, don't use a tickbox at all: just have a "custom" option
- [ ] Save when the page closes
- [ ] Limit the length of the undo history when the garden is loaded/saved
- [ ] Split up the project structure in accordance with the example given [here](https://www.freecodecamp.org/news/how-to-create-a-react-app-with-a-node-backend-the-complete-guide/)
- [ ] When designating clip paths, use the plant's identifier instead of the react-generated identifier
- [ ] Make the start and end points of arrows selectable separately
- [x] There's currently no way of controlling the render order, so rectangles may be placed in front of things that they should not be covering
  - [x] Give beds an "order" property, by which they are sorted

### Bugs

- [ ] When a template is in image mode, loading up its editor defaults to colour mode instead
  - Presumably this is something to do with the dropdown component not setting its initial value properly
  - The rest of the editor's content does load properly, so the state is definitely being saved as it should
- [ ] For some reason, an empty JSON is sometimes saved to the backend
- [ ] Only exclude delect clicks if they move more than eg. two pixels, rather than if they move at all, to make it a little less brittle
- [ ] Keyboard shortcuts don't work until the editor has been focused
- [ ] Numbers should be rounded when they are programmatically updated
- [ ] Somehow prevent multiple tabs' being open from overwriting each others' saves
