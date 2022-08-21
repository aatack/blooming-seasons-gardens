import { configureStore } from "@reduxjs/toolkit";
import produce from "immer";

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
  reducer: (state = { identifier: 1, garden: [], nursery: [] }, action) => {
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
            size: 0.5,
            colour: "#aabbcc",
          };
          const body = action.payload.templateIdentifier
            ? {
                template: action.payload.templateIdentifier,
              }
            : {
                name: action.payload.name
                  ? action.payload.name
                  : "Plant " + state.identifier.toString(),
              };

          bed.elements.push({ ...head, ...body });
        });
      case "garden/plant/removed":
        return produce(state, (draft) => {});
      case "garden/plant/edited":
        return produce(state, (draft) => {});

      default:
        return state;
    }
  },
});

export const addBed = (name) => {
  return { type: "garden/bed/added", payload: name };
};

export const removeBed = (identifier) => {
  return { type: "garden/bed/removed", payload: identifier };
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

export const removeTemplate = (identifier) => {
  return { type: "nursery/template/removed", payload: identifier };
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
