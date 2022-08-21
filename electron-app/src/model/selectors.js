import { useSelector } from "react-redux";

export const useTemplate = (identifier) => {
  return useSelector((state) =>
    state.nursery.find((template) => template.identifier === identifier)
  );
};
