import { useContext, useRef, useState, useEffect } from "react";
import { GardenSVG } from "../../model/context";
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

  const [dragX, setDragX] = useState(0);
  const [dragY, setDragY] = useState(0);
  const [dragging, setDragging] = useState(false);

  const setGardenSVG = useContext(GardenSVG)[1];

  useEffect(() => {
    setGardenSVG(svgElement.current);
  });

  const translate = (dx, dy) => {
    setX(x + dx);
    setY(y + dy);
  };

  const zoom = (fixedX, fixedY, zoom) => {
    const newScale = clamp(scale * zoom, 1 / 100, 100);
    const actualZoom = newScale / scale;

    setX((fixedX + x) / actualZoom - fixedX);
    setY((fixedY + y) / actualZoom - fixedY);

    setScale(newScale);
  };

  const handleClick = () => {
    if (onClick) {
      onClick();
    }
  };

  const handleMouseMove = (e) => {
    if (e.buttons === 1) {
      if (!dragging) {
        setDragging(true);
        setDragX(e.clientX);
        setDragY(e.clientY);
      }
    } else if (dragging) {
      setDragging(false);
    }

    if (dragging) {
      if (e.clientX !== 0 && e.clientY !== 0) {
        translate((e.clientX - dragX) / scale, (e.clientY - dragY) / scale);

        setDragX(e.clientX);
        setDragY(e.clientY);
      }
    }
  };

  const handleWheel = (e) => {
    if (!dragging) {
      const offset = svgElement.current.getBoundingClientRect();
      zoom(
        (e.clientX - offset.x) / scale - x,
        (e.clientY - offset.y) / scale - y,
        1 - e.deltaY * 0.002
      );
    }
  };

  return (
    <div
      onClick={handleClick}
      onMouseMove={handleMouseMove}
      onWheel={handleWheel}
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
