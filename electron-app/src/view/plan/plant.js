import { useContext } from "react";
import { Hovered } from "../../model/context";
import { useTemplate } from "../../model/selectors";

const Plant = ({ plant }) => {
  const hovered = useContext(Hovered);

  const template = useTemplate(plant.template);

  if (template) {
    plant = { ...template, ...plant };
  }

  const handleMouseEnter = () => {
    hovered.set(plant);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  return (
    <circle
      cx={plant.position.x}
      cy={plant.position.y}
      r={plant.size}
      fill={plant.colour}
      stroke={hovered.matches(plant) ? "blue" : "black"}
      strokeWidth={plant.size / (hovered.matches(plant) ? 3 : 5)}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    />
  );
};

export default Plant;
