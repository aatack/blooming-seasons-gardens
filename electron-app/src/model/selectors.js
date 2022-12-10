import { useSelector } from "react-redux";
import { findByIdentifier } from "./store";

export const useNursery = () => {
  return useSelector((state) => state.garden.nursery);
};

export const expandTemplate = (element, nursery) => {
  if (element.template) {
    const template = nursery.find(
      (template) => template.identifier === element.template
    );
    // Template goes first so its identifier is overwritten by the element's
    return { ...template, ...element };
  } else {
    return element;
  }
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
  return useSelector((state) => state.garden.beds)
    .slice()
    .sort((left, right) => {
      if (left.order === right.order) {
        // Identifiers should never be equal
        return left.identifier < right.identifier ? -1 : 1;
      } else {
        return left.order < right.order ? -1 : 1;
      }
    });
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
