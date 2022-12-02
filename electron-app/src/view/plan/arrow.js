import { useContext } from "react";
import { Hovered, Selected } from "../../model/context";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";

const Arrow = ({ arrow }) => {
  const hovered = useContext(Hovered);
  const selected = useContext(Selected);

  const handleMouseEnter = () => {
    hovered.set(arrow);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const handleClick = (e) => {
    selected.set(arrow);
    e.preventDefault();
  };

  const isHovered = hovered.matches(arrow, true);
  const isSelected = selected.matches(arrow, true);

  return (
    <line
      x1={arrow.start.x}
      x2={arrow.end.x}
      y1={arrow.start.y}
      y2={arrow.end.y}
      stroke={
        isHovered ? HOVERED_COLOUR : isSelected ? SELECTED_COLOUR : "black"
      }
      // Scaling by 50 seems to give a reasonable default width; a little bit
      // thicker to highlight it when it's hovered
      strokeWidth={arrow.width / (isHovered ? 30 : 50)}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
    />
  );
};

export default Arrow;
