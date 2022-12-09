import { useContext } from "react";
import { Hovered, Selected } from "../../model/context";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";
import { ClickGroup } from "../common/rendering";

const Rectangle = ({ rectangle }) => {
  const hovered = useContext(Hovered);
  const selected = useContext(Selected);

  const handleMouseEnter = () => {
    hovered.set(rectangle);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const handleClick = () => {
    selected.set(rectangle);
  };

  const isHovered = hovered.matches(rectangle, true);
  const isSelected = selected.matches(rectangle, true);

  return (
    <ClickGroup onClick={handleClick}>
      <line
        x1={rectangle.position.x}
        y1={rectangle.position.y}
        x2={rectangle.size.width}
        y2={rectangle.size.height}
        stroke={
          isHovered ? HOVERED_COLOUR : isSelected ? SELECTED_COLOUR : "black"
        }
        strokeWidth={1}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      />
    </ClickGroup>
  );
};

export default Rectangle;
