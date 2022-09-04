const example = {
  identifier: 29,
  garden: [
    {
      identifier: 3,
      name: "Shady border",
      elements: [
        {
          identifier: 5,
          type: "plant",
          position: { x: 6, y: 1.2 },
          name: "Clover",
          size: 0.05,
          colour: "#005a00",
        },
        {
          identifier: 6,
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
          type: "plant",
          position: { x: 12.04, y: 7 },
          template: 1,
        },
        {
          identifier: 8,
          type: "label",
          position: { x: 13, y: 6 },
          text: "Daffodil",
          size: 12,
        },
        {
          identifier: 9,
          type: "arrow",
          start: { x: 11, y: 8 },
          end: { x: 14, y: 5 },
          width: 1,
        },
      ],
    },
  ],
  nursery: [
    { identifier: 1, name: "Daffodil", size: 0.5, colour: "#f1b7c2" },
    { identifier: 2, name: "Tulip", size: 0.2, colour: "#1a5c96" },
  ],
};

export default example;
