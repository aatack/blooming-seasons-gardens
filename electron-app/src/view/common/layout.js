import { clamp } from "./maths";
import { useState } from "react";

export const HorizontalSplit = ({
  children,
  dragWidth,
  minimumWidth,
  initialWidth,
  toggleKey,
}) => {
  const [first, second] = children.props.children;

  const [width, setWidth] = useState(initialWidth);
  const [x, setX] = useState(null);
  const [collapsed, setCollapsed] = useState(false);

  const handleDragStart = (e) => {
    setX(e.clientX);
  };

  const handleDrag = (e) => {
    if (e.clientX) {
      // TODO: stop the mouse from moving away from the drag box at the extremes
      setWidth(
        clamp(
          width - x + e.clientX,
          minimumWidth,
          window.innerWidth - minimumWidth
        )
      );
      setX(e.clientX);
    }
  };

  const handleClick = () => {
    setCollapsed(!collapsed);
  };

  const handleKeyDown = (e) => {
    if (e.which === toggleKey) {
      setCollapsed(!collapsed);
    }
  };

  return (
    <div onKeyDown={handleKeyDown} tabIndex={0}>
      {!collapsed && (
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
      )}
      <div
        style={{
          position: "fixed",
          height: "100%",
          left: collapsed ? 0 : width,
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
          left: collapsed ? 0 : width - dragWidth,
          width: collapsed ? dragWidth * 2 : dragWidth,
          top: 0,
          cursor: "ew-resize",
        }}
        draggable={true}
        onDragStart={handleDragStart}
        onDrag={handleDrag}
        onClick={handleClick}
      />
    </div>
  );
};
