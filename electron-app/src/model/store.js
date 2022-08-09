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
      default:
        return state;
    }
  },
});
