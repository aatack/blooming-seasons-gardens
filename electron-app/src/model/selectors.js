import { useSelector } from "react-redux";

export const useNursery = () => {
  return useSelector((state) => state.nursery);
};

export const useTemplate = (identifier) => {
  // Returns `null` (not `undefined`) if no template is in use
  return useSelector(
    (state) =>
      state.nursery.find((template) => template.identifier === identifier) ||
      null
  );
};

export const useGarden = () => {
  return useSelector((state) => state);
};

export const useBeds = () => {
  return useSelector((state) => state.garden);
};

export const usePath = () => {
  return useSelector((state) => state.path);
};

export const useBackground = () => {
  return useSelector((state) => state.background);
};
