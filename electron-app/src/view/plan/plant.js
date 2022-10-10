import { useContext } from "react";
import { Hovered } from "../../model/context";
import { useTemplate } from "../../model/selectors";
import { Translate } from "../common/rendering";

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

  const isHovered = hovered.matches(plant, true);

  return (
    <>
      {plant.useColour ? (
        <circle
          cx={plant.position.x}
          cy={plant.position.y}
          r={plant.size / 2} // Size refers to the plant's diameter
          fill={isHovered ? "lightBlue" : plant.colour}
          stroke={isHovered ? "blue" : "black"}
          strokeWidth={plant.size / (isHovered ? 3 : 5)}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        />
      ) : (
        <>
          <Translate x={plant.position.x} y={plant.position.y}>
            <image href={plant.icon.image} />
          </Translate>
        </>
      )}
    </>
  );
};

export default Plant;
