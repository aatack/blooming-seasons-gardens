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

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  };

  const handleDragStart = (e) => {
    // Use an empty image as the ghost image that gets displayed during dragging
    e.dataTransfer.setDragImage(
      document.createElement("img"),
      window.outerWidth,
      window.outerHeight
    );

    setDragX(e.clientX);
    setDragY(e.clientY);

    setDragScale(e.ctrlKey);

    const offset = e.target.getBoundingClientRect();
    setInitialPosition({
      x: e.clientX - offset.x,
      y: e.clientY - offset.y,
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
        const fixedX = initialPosition.x / scale - x;
        const fixedY = initialPosition.y / scale - y;

        const zoom = 1 + -(e.clientY - dragY) * 0.005;
        const newScale = clamp(scale * zoom, 1 / 100, 100);
        const actualZoom = newScale / scale;

        setX((fixedX + x) / actualZoom - fixedX);
        setY((fixedY + y) / actualZoom - fixedY);

        setScale(newScale);
      } else {
        setX(x + (e.clientX - dragX) / scale);
        setY(y + (e.clientY - dragY) / scale);
      }

      setDragX(e.clientX);
      setDragY(e.clientY);
    }
  };

  return (
    <div
      draggable={true}
      onDragStart={handleDragStart}
      onDrag={handleDrag}
      onDragOver={handleDragOver}
      onClick={handleClick}
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
