const emptyGarden = (workspaceIdentifier) => {
  return {
    path: "",
    identifier: 1, // Counter for identifiers assigned to elements
    workspaceIdentifier: workspaceIdentifier, // Identifier of this garden within the workspace
    beds: [],
    nursery: [],
    background: null,
    deleted: false,
  };
};

export default emptyGarden;
