import { useRef, useState } from "react";
import { clamp } from "./maths";

export const SVGViewer = ({
  children,
  initialX,
  initialY,
  initialScale,
  onClick,
}) => {
  const svgElement = useRef();

  const [x, setX] = useState(initialX || 0);
  const [y, setY] = useState(initialY || 0);
  const [scale, setScale] = useState(initialScale || 1);

  const [initialPosition, setInitialPosition] = useState(null);

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
    console.log("Dragging start");
    // Use an empty image as the ghost image that gets displayed during dragging
    // e.dataTransfer.setDragImage(
    //   document.createElement("img"),
    //   window.outerWidth,
    //   window.outerHeight
    // );

    setDragX(e.clientX);
    setDragY(e.clientY);

    setDragScale(e.ctrlKey);

    const offset = e.target.getBoundingClientRect();
    if (initialPosition === null) {
      setInitialPosition({
        x: e.clientX - offset.x,
        y: e.clientY - offset.y,
      });
    }
  };

  const handleClick = () => {
    console.log("On click");
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
      setInitialPosition(null);
    }

    if (dragging) {
      handleDrag(e);
    }
  };

  const handleWheel = (e) => {
    const offset = svgElement.current.getBoundingClientRect();
    console.log(e.deltaY);
    doScale(
      (e.clientX - offset.x) / scale - x,
      (e.clientY - offset.y) / scale - y,
      1 - e.deltaY * 0.002
    );
  };

  return (
    <div
      onWheel={handleWheel}
      onMouseMove={handleMouseMove}
      onClick={handleClick}
      style={{ width: "100%", height: "100%" }}
    >
      <svg ref={svgElement} style={{ width: "100%", height: "100%" }}>
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
