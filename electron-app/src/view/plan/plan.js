import { useBackground, useBeds } from "../../model/selectors";
import { Scale, SVGViewer } from "../common/rendering";
import { useContext, useState } from "react";
import Bed from "./bed";
import { PlanScale, PlanX, PlanY, Selected } from "../../model/context";

const Plan = () => {
  const beds = useBeds();
  const background = useBackground();

  const selected = useContext(Selected);

  const bindX = useContext(PlanX);
  const bindY = useContext(PlanY);
  const bindScale = useContext(PlanScale);

  const handleClick = () => {
    selected.set(null);
  };

  return (
    <SVGViewer
      style={{ width: "100%", height: "100%" }}
      isGardenSVG={true}
      bindX={bindX}
      bindY={bindY}
      bindScale={bindScale}
      onClick={handleClick}
    >
      <Scale scale={50}>
        {background && (
          <Scale scale={background.scale * 0.01}>
            <image href={background.image} />
          </Scale>
        )}

        {beds
          .filter((bed) => !bed.hidden)
          .map((bed) => (
            <Bed bed={bed} key={bed.identifier} />
          ))}
      </Scale>
    </SVGViewer>
  );
};

export default Plan;
