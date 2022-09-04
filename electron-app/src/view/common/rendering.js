import { useState } from "react";
import { clamp } from "./maths";

export const SVGViewer = ({
  children,
  initialX,
  initialY,
  initialScale,
  onClick,
}) => {
  const [x, setX] = useState(initialX || 0);
  const [y, setY] = useState(initialY || 0);
  const [scale, setScale] = useState(initialScale || 1);

  const [initialPosition, setInitialPosition] = useState({ x: 0, y: 0 });

  const [dragX, setDragX] = useState(0);
  const [dragY, setDragY] = useState(0);
  const [dragScale, setDragScale] = useState(false);
  const [dragging, setDragging] = useState(false);

  const doMove = (dx, dy) => {
    setX(x + dx);
    setY(y + dy);
  };

  const doScale = (fixedX, fixedY, zoom) => {
    const newScale = clamp(scale * zoom, 1 / 100, 100);
    const actualZoom = newScale / scale;

    setX((fixedX + x) / actualZoom - fixedX);
    setY((fixedY + y) / actualZoom - fixedY);

    setScale(newScale);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  };

  const handleDragStart = (e) => {
    // Use an empty image as the ghost image that gets displayed during dragging
    // e.dataTransfer.setDragImage(
    //   document.createElement("img"),
    //   window.outerWidth,
    //   window.outerHeight
    // );

    setDragX(e.clientX);
    setDragY(e.clientY);

    setDragScale(e.ctrlKey);

    setInitialPosition({
      x: e.clientX,
      y: e.clientY,
    });
  };

  const handleClick = () => {
    if (onClick) {
      onClick();
    }
  };

  const handleDrag = (e) => {
    if (e.clientX !== 0 && e.clientY !== 0) {
      if (dragScale) {
        doScale(
          initialPosition.x / scale - x,
          initialPosition.y / scale - y,
          1 + -(e.clientY - dragY) * 0.005
        );
      } else {
        doMove((e.clientX - dragX) / scale, (e.clientY - dragY) / scale);
      }

      setDragX(e.clientX);
      setDragY(e.clientY);
    }
  };

  const handleMouseMove = (e) => {
    if (e.buttons == 1) {
      if (!dragging) {
        setDragging(true);
        handleDragStart(e);
      }
    } else if (dragging) {
      setDragging(false);
    }

    if (dragging) {
      handleDrag(e);
    }
  };

  return (
    <div
      // draggable={true}
      // onDragStart={handleDragStart}
      // onDrag={handleDrag}
      // onDragOver={handleDragOver}
      onMouseMove={handleMouseMove}
      // onClick={handleClick}
      style={{ width: "100%", height: "100%" }}
    >
      <svg style={{ width: "100%", height: "100%" }}>
        <Scale scale={scale}>
          <Translate x={x} y={y}>
            {children}
          </Translate>
        </Scale>
      </svg>
    </div>
  );
};

export const Translate = ({ x, y, children }) => {
  return <g transform={`translate(${x || 0}, ${y || 0})`}>{children}</g>;
};

export const Rotate = ({ radians, children }) => {
  return <g transform={`rotate(${radians * (180 / Math.PI)})`}>{children}</g>;
};

export const Scale = ({ scale, children }) => {
  return <g transform={`scale(${scale})`}>{children}</g>;
};
