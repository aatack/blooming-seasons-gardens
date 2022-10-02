import { useContext } from "react";
import { Hovered } from "../../model/context";

const Label = ({ label }) => {
  const hovered = useContext(Hovered);

  const handleMouseEnter = () => {
    hovered.set(label);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const isHovered = hovered.matches(label, true);

  return (
    <text
      x={label.position.x}
      y={label.position.y}
      // Scaling by 10 seems to give reasonable default sizes
      fontSize={label.size / 10}
      fill={isHovered ? "blue" : "black"}
      fontWeight={isHovered ? "bold" : "normal"}
      style={{ userSelect: "none" }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {label.text}
    </text>
  );
};

export default Label;
