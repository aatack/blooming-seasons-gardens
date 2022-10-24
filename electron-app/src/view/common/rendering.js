import { useContext, useRef, useState, useEffect } from "react";
import { GardenSVG } from "../../model/context";
import { clamp } from "./maths";

export const StaticSVG = ({ children }) => {
  // Any elements wrapped in this will not be affected by scales or translations
  // applied by the SVG viewer
  return <g className="static-svg">{children}</g>;
};

export const SVGViewer = ({
  children,
  initialX,
  initialY,
  initialScale,
  onClick,
  isGardenSVG,
}) => {
  // Children should always be wrapped in a React `<> </>` wrapper

  const svgElement = useRef();

  const [x, setX] = useState(initialX || 0);
  const [y, setY] = useState(initialY || 0);
  const [scale, setScale] = useState(initialScale || 1);

  const [dragX, setDragX] = useState(0);
  const [dragY, setDragY] = useState(0);
  const [dragging, setDragging] = useState(false);

  const setGardenSVG = useContext(GardenSVG)[1];

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

  useEffect(() => {
    if (isGardenSVG) {
      setGardenSVG(svgElement.current);
    }

    const cancelWheel = (e) => {
      e.preventDefault();
    };

    // By default, React uses passive event handlers, which are not allowed to
    // stop propgagation.  So we have to use the ref to attach the `onWheel`
    // handler to the SVG element
    if (svgElement && svgElement.current) {
      svgElement.current.addEventListener("wheel", cancelWheel, {
        passive: false,
      });
      return () => {
        if (svgElement.current) {
          svgElement.current.removeEventListener("wheel", cancelWheel);
        }
      };
    }
  }, []);

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

  const isStatic = (child) => {
    if (child && child.type && child.type.name) {
      return child.type.name;
    } else {
      return null;
    }
  };

  const dynamicChildren = children.props.children.filter((c) => !isStatic(c));
  const staticChildren = children.props.children.filter(isStatic);

  return (
    <div
      onClick={handleClick}
      onMouseMove={handleMouseMove}
      style={{ width: "100%", height: "100%" }}
    >
      <svg
        ref={svgElement}
        style={{ width: "100%", height: "100%" }}
        onWheel={handleWheel}
      >
        <Scale scale={scale}>
          <Translate x={x} y={y}>
            {dynamicChildren}
          </Translate>
        </Scale>

        {staticChildren}
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
