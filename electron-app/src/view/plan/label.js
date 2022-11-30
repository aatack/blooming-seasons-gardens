import { useContext } from "react";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";
import { Hovered, Selected } from "../../model/context";

const Label = ({ label }) => {
  const hovered = useContext(Hovered);
  const selected = useContext(Selected);

  const handleMouseEnter = () => {
    hovered.set(label);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const handleClick = () => {
    selected.set(label);
  };

  const isHovered = hovered.matches(label, true);
  const isSelected = selected.matches(label, true);

  return (
    <text
      className="blooming-seasons-gardens-element"
      x={label.position.x}
      y={label.position.y}
      // Scaling by 10 seems to give reasonable default sizes
      fontSize={label.size / 10}
      fill={isHovered ? HOVERED_COLOUR : isSelected ? SELECTED_COLOUR : "black"}
      style={{ userSelect: "none" }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
    >
      {label.text}
    </text>
  );
};

export default Label;
