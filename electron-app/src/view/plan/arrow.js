import { useContext } from "react";
import { Hovered } from "../../model/context";

const Arrow = ({ arrow }) => {
  const hovered = useContext(Hovered);

  const handleMouseEnter = () => {
    hovered.set(arrow);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const isHovered = hovered.matches(arrow, true);

  return (
    <line
      x1={arrow.start.x}
      x2={arrow.end.x}
      y1={arrow.start.y}
      y2={arrow.end.y}
      stroke={isHovered ? "blue" : "black"}
      // Scaling by 50 seems to give a reasonable default width; a little bit
      // thicker to highlight it when it's hovered
      strokeWidth={arrow.width / (isHovered ? 30 : 50)}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    />
  );
};

export default Arrow;
