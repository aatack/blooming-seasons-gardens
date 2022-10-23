import { useBackground, useBeds } from "../../model/selectors";
import { Scale, SVGViewer } from "../common/rendering";
import Bed from "./bed";

const Plan = () => {
  const beds = useBeds();
  const background = useBackground();

  return (
    <SVGViewer style={{ width: "100%", height: "100%" }} isGardenSVG={true}>
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
