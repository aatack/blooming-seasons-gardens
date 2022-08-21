import { configureStore } from "@reduxjs/toolkit";
import produce from "immer";

export const store = configureStore({
  reducer: (state = { identifier: 0, garden: [], nursery: [] }, action) => {
    switch (action.type) {
      case "garden/bed/added":
        return produce(state, (draft) => {
          draft.identifier += 1;
          draft.garden.push({
            identifier: state.identifier,
            name: action.payload
              ? action.payload
              : "Bed " + state.identifier.toString(),
          });
        });
      case "garden/bed/removed":
        return produce(state, (draft) => {
          draft.garden = state.garden.filter(
            (bed) => bed.identifier !== action.payload
          );
        });
      case "garden/bed/renamed":
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
            size: "5", // TODO: change sizes to numbers
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
