import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: (state = { value: 0 }, action) => {
    switch (action.type) {
      case "incremented":
        return { value: state.value + 1 };
      case "decremented":
        return { value: state.value - 1 };
      default:
        return state;
    }
  },
});
