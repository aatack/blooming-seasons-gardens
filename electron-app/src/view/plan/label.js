import { useContext } from "react";
import { Hovered } from "../../model/context";

const Label = ({ label }) => {
  const hovered = useContext(Hovered);

  return (
    <text
      x={label.position.x}
      y={label.position.y}
      // Scaling by 10 seems to give reasonable default sizes
      fontSize={label.size / 10}
      fill={hovered.matches(label) ? "blue" : "black"}
      fontWeight={hovered.matches(label) ? "bold" : "normal"}
      style={{ userSelect: "none" }}
    >
      {label.text}
    </text>
  );
};

export default Label;
