const exampleGarden = {
  garden: {
    path: "Example Garden",
    identifier: 29,
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
    // garden state.  If the index is `null`, we are up to date and therefore
    // the current state has not yet been added to the history's items
    index: null,

    // Only stores garden states that have been superseded by another, ie. the
    // most up-to-date garden state is not in the list of items unless we are
    // accessing the history directly
    items: [],
  },
};

export default exampleGarden;
