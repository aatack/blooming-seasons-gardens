import { useContext } from "react";
import { Hovered } from "../../model/context";
import { useTemplate } from "../../model/selectors";
import { Scale, Translate } from "../common/rendering";

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
      {plant.iconMode === "colour" ? (
        <circle
          cx={plant.position.x}
          cy={plant.position.y}
          r={plant.size / 2} // Size refers to the plant's diameter
          fill={isHovered ? "lightBlue" : plant.iconColour}
          stroke={isHovered ? "blue" : "black"}
          strokeWidth={plant.size / (isHovered ? 3 : 5)}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        />
      ) : (
        // When scaling and positioning the image, the user moves it into a
        // circle with a radius of 100 units positioned at (120, 120).  So to
        // properly render it here, we apply the transforms that they saved, and
        // then perform those that would move that circle to one centred at
        // (0, 0) with a radius matching that specified for the plant
        <>
          <Translate x={plant.position.x} y={plant.position.y}>
            {/* TODO: combine the various nested transforms into one */}
            <Scale scale={0.01 * (plant.size / 2)}>
              <Translate x={-120} y={-120}>
                <Scale scale={plant.iconScale}>
                  <Translate x={plant.iconX} y={plant.iconY}>
                    <image href={plant.iconImage} />
                  </Translate>
                </Scale>
              </Translate>
            </Scale>
          </Translate>

          <circle
            cx={plant.position.x}
            cy={plant.position.y}
            r={plant.size / 2} // Size refers to the plant's diameter
            // If fill or stroke are `none` then mouseover does not work
            fill="rgba(0, 0, 0, 0)"
            stroke={isHovered ? "blue" : "rgba(0, 0, 0, 0)"}
            strokeWidth={plant.size / 5}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
          />
        </>
      )}
    </>
  );
};

export default Plant;
