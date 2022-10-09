const emptyGarden = (workspaceIdentifier, name) => {
  return {
    path: name,
    // Counter for identifiers assigned to elements
    identifier: 1,
    // Identifier of this garden within the workspace
    workspaceIdentifier: workspaceIdentifier,
    beds: [],
    nursery: [],
    background: null,
    deleted: false,
  };
};

export default emptyGarden;
