import { Scale, SVGViewer } from "../common/rendering";
import Bed from "./bed";
import { useSelector } from "react-redux";

const Plan = () => {
  const garden = useSelector((state) => state.garden);

  return (
    <SVGViewer style={{ width: "100%", height: "100%" }}>
      <Scale scale={50}>
        {garden.map((bed) => (
          <Bed bed={bed} key={bed.identifier} />
        ))}
      </Scale>
    </SVGViewer>
  );
};

export default Plan;
