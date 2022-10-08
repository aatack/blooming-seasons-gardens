import { useSelector } from "react-redux";

export const useNursery = () => {
  return useSelector((state) => state.garden.nursery);
};

export const useTemplate = (identifier) => {
  // Returns `null` (not `undefined`) if no template is in use
  return useSelector(
    (state) =>
      state.garden.nursery.find(
        (template) => template.identifier === identifier
      ) || null
  );
};

export const useGarden = () => {
  return useSelector((state) => state.garden);
};

export const useBeds = () => {
  return useSelector((state) => state.garden.beds);
};

export const usePath = () => {
  return useSelector((state) => state.garden.path);
};

export const useBackground = () => {
  return useSelector((state) => state.garden.background);
};
