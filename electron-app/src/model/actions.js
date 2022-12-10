export const undo = () => {
  return { type: "undo" };
};

export const redo = () => {
  return { type: "redo" };
};

export const workspacePushed = () => {
  return { type: "workspace/pushed" };
};

export const workspacePulled = (identifier) => {
  return { type: "workspace/pulled", payload: identifier };
};

export const workspaceCopied = (identifier) => {
  return { type: "workspace/copied", payload: identifier };
};

export const workspaceDeleted = (identifier) => {
  return { type: "workspace/deleted", payload: identifier };
};

export const workspaceCreated = (path) => {
  return { type: "workspace/created", payload: path };
};

export const renameGarden = (newName) => {
  return { type: "garden/renamed", payload: newName };
};

export const addBed = (name) => {
  return { type: "garden/bed/added", payload: name };
};

export const removeBed = (bed) => {
  return { type: "garden/bed/removed", payload: bed.identifier };
};

export const editBed = (identifier, name, order) => {
  return {
    type: "garden/bed/edited",
    payload: { identifier: identifier, name: name, order: order },
  };
};

export const hideBed = (identifier, hidden) => {
  return {
    type: "garden/bed/hidden",
    payload: { identifier: identifier, hidden: hidden },
  };
};

export const addPlantTemplate = (name) => {
  return {
    type: "nursery/template/added",
    payload: {
      type: "plant",
      name: name,
      size: 0.5,
      border: 0.02,
      iconMode: "colour",
      iconColour: "#aabbcc",
      iconImage: null,
      iconScale: 1,
      iconX: 0,
      iconY: 0,
    },
  };
};

export const addLabelTemplate = (text) => {
  return {
    type: "nursery/template/added",
    payload: { type: "label", text: text, size: 12, font: "Arial" },
  };
};

export const removeTemplate = (template) => {
  return { type: "nursery/template/removed", payload: template.identifier };
};

export const editTemplate = (identifier, edits) => {
  return {
    type: "nursery/template/edited",
    payload: {
      identifier: identifier,
      edits: edits,
    },
  };
};

export const addTemplatePlant = (bed, template) => {
  return {
    type: "garden/plant/added",
    payload: {
      bedIdentifier: bed.identifier,
      templateIdentifier: template.identifier,
    },
  };
};

export const addCustomPlant = (bed, name) => {
  return {
    type: "garden/plant/added",
    payload: { bedIdentifier: bed.identifier, name: name },
  };
};

export const addTemplateLabel = (bed, template) => {
  return {
    type: "garden/label/added",
    payload: {
      bedIdentifier: bed.identifier,
      templateIdentifier: template.identifier,
    },
  };
};

export const addCustomLabel = (bed, text) => {
  return {
    type: "garden/label/added",
    payload: { bedIdentifier: bed.identifier, text: text },
  };
};

export const addArrow = (bed) => {
  return {
    type: "garden/arrow/added",
    payload: {
      bedIdentifier: bed.identifier,
      start: { x: 0, y: 0 },
      end: { x: 1, y: 1 },
    },
  };
};

export const addRectangle = (bed) => {
  return {
    type: "garden/rectangle/added",
    payload: {
      bedIdentifier: bed.identifier,
      position: { x: 0.0, y: 0.0 },
      size: { width: 1.0, height: 1.0 },
      colour: "#ffffff",
    },
  };
};

export const removeElement = (element) => {
  return { type: "garden/element/removed", payload: element.identifier };
};

export const editElement = (element, edits) => {
  return {
    type: "garden/element/edited",
    payload: {
      identifier: element.identifier,
      edits: edits,
    },
  };
};

export const copyElement = (element) => {
  return {
    type: "garden/element/copied",
    payload: element.identifier,
  };
};

export const setBackground = (image, scale) => {
  // Expects the image to be passed as a string data URL, but may also be null
  return {
    type: "garden/background/set",
    payload: { image: image, scale: scale },
  };
};

export const removeBackground = () => {
  return { type: "garden/background/removed" };
};
