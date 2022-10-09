import { configureStore } from "@reduxjs/toolkit";
import produce from "immer";
import emptyGarden from "./empty";
import exampleGarden from "./example";

const findByIdentifier = (state, identifier) => {
  for (const bed of state.beds) {
    if (bed.identifier === identifier) {
      return bed;
    }

    for (const element of bed.elements) {
      if (element.identifier === identifier) {
        return element;
      }
    }
  }

  for (const template of state.nursery) {
    if (template.identifier === identifier) {
      return template;
    }
  }

  return null;
};

const produceWithHistory = (state, transform) => {
  // TODO: ensure none of the current reducers access the state directly,
  //       assuming it to be distinct from the draft
  return produce(state, (draft) => {
    if (!state.history.items.length) {
      draft.history.index = 0;
      draft.history.items = [state.garden];
    }

    transform(draft.garden);

    // Clear out any "alternative timelines"
    draft.history.items.splice(draft.history.index + 1);
    draft.history.index++;
    draft.history.items.push(draft.garden);
  });
};

export const store = configureStore({
  // Start the identifier at 1 so we can guarantee the it will never be zero,
  // and can therefore cast identifiers to booleans to see whether they exist
  reducer: (state = exampleGarden, action) => {
    switch (action.type) {
      case "initialised":
        return produceWithHistory(state, (draft) => action.payload);

      case "workspace/created":
        // Overrides the current garden; should only be used after pushing the
        // current garden, ie. from the choose garden screen
        return produce(state, (draft) => {
          draft.workspace.identifier += 1;
          draft.garden = emptyGarden(
            state.workspace.identifier,
            action.payload
          );

          draft.history.items = [draft.garden];
          draft.history.index = 0;
        });
      case "workspace/pushed":
        return produce(state, (draft) => {
          draft.workspace.gardens.push(state.garden);
          draft.garden = null;
        });
      case "workspace/copied":
        return produce(state, (draft) => {
          const gardenNames = state.workspace.gardens
            .filter((garden) => !garden.deleted)
            .map((garden) => garden.path);
          const garden = state.workspace.gardens.find(
            (garden) => garden.workspaceIdentifier === action.payload
          );

          var index = 1;
          var attempt = `${garden.path} (copy ${index})`;
          while (gardenNames.indexOf(attempt) !== -1) {
            index++;
            attempt = `${garden.path} (copy ${index})`;
          }

          draft.workspace.identifier += 1;
          draft.workspace.gardens.push({
            ...garden,
            path: attempt,
            workspaceIdentifier: state.workspace.identifier,
          });
        });
      case "workspace/pulled":
        return produce(state, (draft) => {
          // Pop the active garden out of the workspace
          draft.garden = state.workspace.gardens.find(
            (garden) => garden.workspaceIdentifier === action.payload
          );
          draft.workspace.gardens = draft.workspace.gardens.filter(
            (garden) => garden.workspaceIdentifier !== action.payload
          );

          draft.history.items = [draft.garden];
          draft.history.index = 0;
        });
      case "workspace/deleted":
        return produce(state, (draft) => {
          const garden = draft.workspace.gardens.find(
            (garden) => garden.workspaceIdentifier === action.payload
          );
          garden.deleted = true;
        });

      case "undo":
        // TODO: assert that the ;ength of the history items is above zero
        return produce(state, (draft) => {
          if (draft.history.index > 0) {
            draft.history.index--;
          }
          draft.garden = draft.history.items[draft.history.index];
        });
      case "redo":
        // TODO: assert that the history index strictly less than the current
        //       length of the items array minus one
        return produce(state, (draft) => {
          const length = draft.history.items.length || 1;

          draft.history.index++;
          if (draft.history.index >= length) {
            draft.history.index = length - 1;
          }

          draft.garden = draft.history.items[draft.history.index];
        });

      case "garden/renamed":
        return produceWithHistory(state, (draft) => {
          draft.path = action.payload;
        });

      case "garden/bed/added":
        return produceWithHistory(state, (draft) => {
          draft.identifier += 1;
          draft.beds.push({
            identifier: state.garden.identifier,
            name: action.payload
              ? action.payload
              : "Bed " + state.garden.identifier.toString(),
            elements: [],
          });
        });
      case "garden/bed/removed":
        return produceWithHistory(state, (draft) => {
          draft.beds = state.garden.beds.filter(
            (bed) => bed.identifier !== action.payload
          );
        });
      case "garden/bed/renamed": // TODO: make this "edited" instead
        return produceWithHistory(state, (draft) => {
          const bed = draft.beds.find(
            (b) => b.identifier === action.payload.identifier
          );
          bed.name = action.payload.name;
        });

      case "nursery/template/added":
        return produceWithHistory(state, (draft) => {
          draft.identifier += 1;
          draft.nursery.push({
            identifier: state.garden.identifier,
            name: action.payload
              ? action.payload
              : "Template " + state.garden.identifier.toString(),
            size: 0.5,
            colour: "#aabbcc",
          });
        });
      case "nursery/template/removed":
        return produceWithHistory(state, (draft) => {
          // TODO: remove dependent elements
          draft.nursery = draft.nursery.filter(
            (template) => template.identifier !== action.payload
          );
        });
      case "nursery/template/edited":
        return produceWithHistory(state, (draft) => {
          const template = draft.nursery.find(
            (t) => t.identifier === action.payload.identifier
          );
          template.name = action.payload.name;
          template.size = action.payload.size;
          template.colour = action.payload.colour;
        });

      case "garden/plant/added":
        return produceWithHistory(state, (draft) => {
          draft.identifier += 1;
          const bed = findByIdentifier(draft, action.payload.bedIdentifier);

          const head = {
            identifier: state.garden.identifier,
            bedIdentifier: action.payload.bedIdentifier,
            type: "plant",
            position: { x: 0, y: 0 },
          };
          const body = action.payload.templateIdentifier
            ? {
                template: action.payload.templateIdentifier,
              }
            : {
                name: action.payload.name
                  ? action.payload.name
                  : "Plant " + state.garden.identifier.toString(),
                size: 0.5,
                colour: "#aabbcc",
              };

          bed.elements.push({ ...head, ...body });
        });

      case "garden/label/added":
        return produceWithHistory(state, (draft) => {
          draft.identifier += 1;
          const bed = findByIdentifier(draft, action.payload.bedIdentifier);

          bed.elements.push({
            identifier: state.garden.identifier,
            bedIdentifier: action.payload.bedIdentifier,
            type: "label",
            text: action.payload.text
              ? action.payload.text
              : "Label " + state.garden.identifier.toString(),
            position: { x: 0, y: 0 },
            size: 12,
          });
        });

      case "garden/arrow/added":
        return produceWithHistory(state, (draft) => {
          draft.identifier += 1;
          const bed = findByIdentifier(draft, action.payload.bedIdentifier);

          bed.elements.push({
            identifier: state.garden.identifier,
            bedIdentifier: action.payload.bedIdentifier,
            type: "arrow",
            start: action.payload.start,
            end: action.payload.end,
            width: 4,
          });
        });

      case "garden/element/removed":
        return produceWithHistory(state, (draft) => {
          for (const bed of draft.beds) {
            if (
              bed.elements.find(
                (element) => element.identifier === action.payload
              )
            ) {
              bed.elements = bed.elements.filter(
                (element) => element.identifier !== action.payload
              );
            }
          }
        });
      case "garden/element/edited":
        return produceWithHistory(state, (draft) => {
          const element = findByIdentifier(draft, action.payload.identifier);

          for (const key in action.payload.edits) {
            element[key] = action.payload.edits[key];
          }
        });

      case "garden/background/set":
        return produceWithHistory(state, (draft) => {
          draft.background = action.payload;
        });
      case "garden/background/removed":
        return produceWithHistory(state, (draft) => {
          draft.background = null;
        });

      default:
        return state;
    }
  },
});
