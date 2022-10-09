const exampleGarden = {
  garden: {
    path: "Example Garden",
    identifier: 29, // Counter for identifiers assigned to elements
    workspaceIdentifier: 1, // Identifier of this garden within the workspace
    beds: [
      {
        identifier: 3,
        name: "Shady border",
        elements: [
          {
            identifier: 5,
            bedIdentifier: 3,
            type: "plant",
            position: { x: 6, y: 1.2 },
            name: "Clover",
            size: 0.05,
            colour: "#005a00",
          },
          {
            identifier: 6,
            bedIdentifier: 3,
            type: "plant",
            position: { x: -5, y: 4 },
            template: 2,
          },
        ],
      },
      {
        identifier: 4,
        name: "Flower pot",
        elements: [
          {
            identifier: 7,
            bedIdentifier: 4,
            type: "plant",
            position: { x: 12.04, y: 7 },
            template: 1,
          },
          {
            identifier: 8,
            bedIdentifier: 4,
            type: "label",
            position: { x: 13, y: 6 },
            text: "Daffodil",
            size: 12,
          },
          {
            identifier: 9,
            bedIdentifier: 4,
            type: "arrow",
            start: { x: 11, y: 8 },
            end: { x: 14, y: 5 },
            width: 4,
          },
        ],
      },
    ],
    nursery: [
      { identifier: 1, name: "Daffodil", size: 0.5, colour: "#f1b7c2" },
      { identifier: 2, name: "Tulip", size: 0.2, colour: "#1a5c96" },
    ],
    background: null,
  },
  history: {
    // Points to the index, within the items below, of the currently inspected
    // garden state
    index: 0,

    // Stores all previous iterations of the garden (within the current session)
    // in an array.  The one currently displayed is almost always the one within
    // this list at the index described above, with the excetpion of transitory
    // states (eg. when a value is changed continuously but will ultimately be
    // viewed as a single action for the purposes of undoing).  In theory the
    // array should never be empty, so will have the current state added to it
    // before any changes take place, since it is initialised as empty.
    items: [],
  },
  workspace: {
    identifier: 1, // Next identifier to be assigned to a garden
    gardens: [
      /* 
      
      List of saved garden objects something like the following:
      
      {
        identifier: int,
        garden: Garden (see above),
        deleted: bool
      }

      It might be useful to enforce that there are no duplicate paths.

      */
    ],
  },
};

export default exampleGarden;
