import { useBackground, useBeds } from "../../model/selectors";
import { Scale, SVGViewer } from "../common/rendering";
import { useContext, useState } from "react";
import Bed from "./bed";
import { Selected } from "../../model/context";

const Plan = () => {
  const beds = useBeds();
  const background = useBackground();

  const selected = useContext(Selected);

  const bindX = useState(0);
  const bindY = useState(0);
  const bindScale = useState(100);

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

        {beds.map((bed) => (
          <Bed bed={bed} key={bed.identifier} />
        ))}
      </Scale>
    </SVGViewer>
  );
};

export default Plan;
