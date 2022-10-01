import { useContext } from "react";
import { Hovered } from "../../model/context";

const Arrow = ({ arrow }) => {
  const hovered = useContext(Hovered);

  return (
    <line
      x1={arrow.start.x}
      x2={arrow.end.x}
      y1={arrow.start.y}
      y2={arrow.end.y}
      stroke={hovered.matches(arrow) ? "blue" : "black"}
      // Scaling by 50 seems to give a reasonable default width
      strokeWidth={arrow.width / (hovered.matches(arrow) ? 30 : 50)}
    />
  );
};

export default Arrow;
