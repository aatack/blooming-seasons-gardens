import { useContext } from "react";
import { Hovered, Selected } from "../../model/context";
import { useTemplate } from "../../model/selectors";
import { Scale, Translate } from "../common/rendering";
import { useId } from "react";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";

const Plant = ({ plant }) => {
  const hovered = useContext(Hovered);
  const selected = useContext(Selected);
  const clipPathIdentifier = useId();

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

  const handleClick = () => {
    selected.set(plant);
  };

  const isHovered = hovered.matches(plant, true);
  const isSelected = selected.matches(plant, true);

  // Size refers to the plant's diameter
  const radius = plant.size / 2;
  const border =
    (plant.border > radius ? radius : plant.border) * (isSelected ? 2 : 1);

  return (
    <>
      {plant.iconMode === "colour" ? (
        <circle
          cx={plant.position.x}
          cy={plant.position.y}
          r={radius - border / 2}
          fill={plant.iconColour}
          stroke={
            isHovered ? HOVERED_COLOUR : isSelected ? SELECTED_COLOUR : "black"
          }
          strokeWidth={border}
          onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
          onClick={handleClick}
        />
      ) : (
        // When scaling and positioning the image, the user moves it into a
        // circle with a radius of 100 units positioned at (120, 120).  So to
        // properly render it here, we apply the transforms that they saved, and
        // then perform those that would move that circle to one centred at
        // (0, 0) with a radius matching that specified for the plant
        <>
          <clipPath id={clipPathIdentifier}>
            <circle
              cx={plant.position.x}
              cy={plant.position.y}
              r={plant.size / 2}
            />
          </clipPath>
          <g clipPath={`url(#${clipPathIdentifier})`}>
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
              r={radius - border / 2}
              // If fill or stroke are `none` then mouseover does not work
              fill="rgba(0, 0, 0, 0)"
              stroke={
                isHovered
                  ? HOVERED_COLOUR
                  : isSelected
                  ? SELECTED_COLOUR
                  : "rgba(0, 0, 0, 0)"
              }
              strokeWidth={border}
              onMouseEnter={handleMouseEnter}
              onMouseLeave={handleMouseLeave}
              onClick={handleClick}
            />
          </g>
        </>
      )}
    </>
  );
};

export default Plant;
