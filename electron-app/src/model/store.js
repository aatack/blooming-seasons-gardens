import { configureStore } from "@reduxjs/toolkit";
import produce from "immer";
import example from "./example";

const findByIdentifier = (state, identifier) => {
  for (const bed of state.garden) {
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

export const store = configureStore({
  // Start the identifier at 1 so we can guarantee the it will never be zero,
  // and can therefore cast identifiers to booleans to see whether they exist
  reducer: (state = example, action) => {
    switch (action.type) {
      case "garden/bed/added":
        return produce(state, (draft) => {
          draft.identifier += 1;
          draft.garden.push({
            identifier: state.identifier,
            name: action.payload
              ? action.payload
              : "Bed " + state.identifier.toString(),
            elements: [],
          });
        });
      case "garden/bed/removed":
        return produce(state, (draft) => {
          draft.garden = state.garden.filter(
            (bed) => bed.identifier !== action.payload
          );
        });
      case "garden/bed/renamed": // TODO: make this "edited" instead
        return produce(state, (draft) => {
          const bed = draft.garden.find(
            (b) => b.identifier === action.payload.identifier
          );
          bed.name = action.payload.name;
        });

      case "nursery/template/added":
        return produce(state, (draft) => {
          draft.identifier += 1;
          draft.nursery.push({
            identifier: state.identifier,
            name: action.payload
              ? action.payload
              : "Template " + state.identifier.toString(),
            size: 0.5,
            colour: "#aabbcc",
          });
        });
      case "nursery/template/removed":
        return produce(state, (draft) => {
          // TODO: remove dependent elements
          draft.nursery = draft.nursery.filter(
            (template) => template.identifier !== action.payload
          );
        });
      case "nursery/template/edited":
        return produce(state, (draft) => {
          const template = draft.nursery.find(
            (t) => t.identifier === action.payload.identifier
          );
          template.name = action.payload.name;
          template.size = action.payload.size;
          template.colour = action.payload.colour;
        });

      case "garden/plant/added":
        return produce(state, (draft) => {
          draft.identifier += 1;
          const bed = findByIdentifier(draft, action.payload.bedIdentifier);

          const head = {
            identifier: state.identifier,
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
                  : "Plant " + state.identifier.toString(),
                size: 0.5,
                colour: "#aabbcc",
              };

          bed.elements.push({ ...head, ...body });
        });

      case "garden/label/added":
        return produce(state, (draft) => {
          draft.identifier += 1;
          const bed = findByIdentifier(draft, action.payload.bedIdentifier);

          bed.elements.push({
            identifier: state.identifier,
            type: "label",
            text: action.payload.text
              ? action.payload.text
              : "Label " + state.identifier.toString(),
            position: { x: 0, y: 0 },
            size: 12,
          });
        });

      case "garden/arrow/added":
        return produce(state, (draft) => {
          draft.identifier += 1;
          const bed = findByIdentifier(draft, action.payload.bedIdentifier);

          bed.elements.push({
            identifier: state.identifier,
            type: "arrow",
            start: action.payload.start,
            end: action.payload.end,
            width: 4,
          });
        });

      case "garden/element/removed":
        return produce(state, (draft) => {
          for (const bed of draft.garden) {
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
        return produce(state, (draft) => {
          const element = findByIdentifier(draft, action.payload.identifier);

          for (const key in action.payload.edits) {
            element[key] = action.payload.edits[key];
          }
        });

      case "garden/background/changed":
        return produce(state, (draft) => {
          if (!draft.background) {
            draft.background = { image: action.payload, width: 10 };
          } else {
            draft.background.image = action.payload;
          }
        });

      default:
        return state;
    }
  },
});

export const addBed = (name) => {
  return { type: "garden/bed/added", payload: name };
};

export const removeBed = (bed) => {
  return { type: "garden/bed/removed", payload: bed.identifier };
};

export const renameBed = (identifier, name) => {
  return {
    type: "garden/bed/renamed",
    payload: { identifier: identifier, name: name },
  };
};

export const addTemplate = (name) => {
  return { type: "nursery/template/added", payload: name };
};

export const removeTemplate = (template) => {
  return { type: "nursery/template/removed", payload: template.identifier };
};

export const editTemplate = (identifier, name, size, colour) => {
  return {
    type: "nursery/template/edited",
    payload: {
      identifier: identifier,
      name: name,
      size: size,
      colour: colour,
    },
  };
};

export const addTemplatePlant = (bed, template) => {
  return {
    type: "garden/plant/added",
    payload: {
      bedIdentifier: bed.identifier,
      templateIdentifier: template.identifier,
    },
  };
};

export const addCustomPlant = (bed, name) => {
  return {
    type: "garden/plant/added",
    payload: { bedIdentifier: bed.identifier, name: name },
  };
};

export const addLabel = (bed, text) => {
  return {
    type: "garden/label/added",
    payload: { bedIdentifier: bed.identifier, text: text },
  };
};

export const addArrow = (bed) => {
  return {
    type: "garden/arrow/added",
    payload: {
      bedIdentifier: bed.identifier,
      start: { x: 0, y: 0 },
      end: { x: 1, y: 1 },
    },
  };
};

export const removeElement = (element) => {
  return { type: "garden/element/removed", payload: element.identifier };
};

export const editElement = (element, edits) => {
  return {
    type: "garden/element/edited",
    payload: {
      identifier: element.identifier,
      edits: edits,
    },
  };
};

export const changeBackground = (image) => {
  // Expects a string describing the data URL of the image; see `encodeFile`
  return {
    type: "garden/background/changed",
    payload: image,
  };
};
