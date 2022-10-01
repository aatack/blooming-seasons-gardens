import { useSelector } from "react-redux";

export const useTemplate = (identifier) => {
  // Returns `null` (not `undefined`) if no template is in use
  return useSelector(
    (state) =>
      state.nursery.find((template) => template.identifier === identifier) ||
      null
  );
};
