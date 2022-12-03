import { useSelector } from "react-redux";
import { findByIdentifier } from "./store";

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

export const useElement = (identifier) => {
  return useSelector((state) => {
    return identifier === null
      ? null
      : findByIdentifier(state.garden, identifier);
  });
};

export const useLoaded = () => {
  return useSelector((state) => state !== null);
};

export const useGarden = () => {
  return useSelector((state) => (state === null ? null : state.garden));
};

export const useGardens = () => {
  return useSelector((state) => {
    const gardens = state.workspace.gardens.filter((garden) => !garden.deleted);
    gardens.sort((left, right) => left.path.localeCompare(right.path));
    return gardens;
  });
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

export const useUndoAvailable = () => {
  return useSelector((state) => state.history.index > 0);
};

export const useRedoAvailable = () => {
  return useSelector(
    (state) => state.history.index < (state.history.items.length || 1) - 1
  );
};
