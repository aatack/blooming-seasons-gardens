import { useContext } from "react";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";
import { Hovered, Selected } from "../../model/context";
import { ClickGroup } from "../common/rendering";

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

  const lines = label.text.split("\n");

  return (
    <ClickGroup onClick={handleClick}>
      <text
        textAnchor="middle"
        x={label.position.x}
        y={label.position.y}
        // Scaling by 10 seems to give reasonable default sizes
        fontSize={label.size / 10}
        fill={
          isHovered ? HOVERED_COLOUR : isSelected ? SELECTED_COLOUR : "black"
        }
        style={{ userSelect: "none", fontFamily: label.font }}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {lines.map((line) => (
          <tspan x="0" dy="1.2em">
            {line}
          </tspan>
        ))}
      </text>
    </ClickGroup>
  );
};

export default Label;
