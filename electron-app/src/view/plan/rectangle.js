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
      <rect
        x={rectangle.position.x}
        y={rectangle.position.y}
        width={rectangle.size.width}
        height={rectangle.size.height}
        style={{
          fill: isHovered
            ? HOVERED_COLOUR
            : isSelected
            ? SELECTED_COLOUR
            : rectangle.colour,
        }}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      />
    </ClickGroup>
  );
};

export default Rectangle;
