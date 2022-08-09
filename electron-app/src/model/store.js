import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: (state = { identifier: 0, garden: [], nursery: [] }, action) => {
    switch (action.type) {
      case "garden/bed/added":
        return {
          ...state,
          identifier: state.identifier + 1,
          garden: [
            ...state.garden,
            {
              identifier: state.identifier,
              name: action.payload
                ? action.payload
                : "Bed " + state.identifier.toString(),
            },
          ],
        };
      default:
        return state;
    }
  },
});
