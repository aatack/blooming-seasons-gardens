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

  return (
    <text
      x={label.position.x}
      y={label.position.y}
      // Scaling by 10 seems to give reasonable default sizes
      fontSize={label.size / 10}
      fill={hovered.matches(label) ? "blue" : "black"}
      fontWeight={hovered.matches(label) ? "bold" : "normal"}
      style={{ userSelect: "none" }}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {label.text}
    </text>
  );
};

export default Label;
