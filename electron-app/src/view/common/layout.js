import { useState } from "react";

export const HorizontalSplit = ({ children, dragWidth }) => {
  const [first, second] = children.props.children;

  const [width, setWidth] = useState(window.innerWidth * 0.3);
  const [x, setX] = useState(null);

  const handleDragStart = (e) => {
    setX(e.clientX);
  };

  const handleDrag = (e) => {
    if (e.clientX) {
      setWidth(width - x + e.clientX);
      setX(e.clientX);
    }
  };

  return (
    <>
      <div
        style={{
          position: "fixed",
          height: "100%",
          left: "0%",
          width: width,
          top: "0%",
        }}
      >
        {first}
      </div>
      <div
        style={{
          position: "fixed",
          height: "100%",
          left: width,
          right: "0%",
          top: 0,
        }}
      >
        {second}
      </div>
      <div
        style={{
          position: "fixed",
          height: "100%",
          left: width - dragWidth / 2,
          width: dragWidth,
          top: 0,
          cursor: "ew-resize",
        }}
        draggable={true}
        onDragStart={handleDragStart}
        onDrag={handleDrag}
      />
    </>
  );
};
