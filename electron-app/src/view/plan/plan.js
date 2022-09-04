import { useState } from "react";
import { SVGViewer } from "../common/rendering";

const Plan = () => {
  const [x, setX] = useState(0);
  const [y, setY] = useState(0);

  const handleWheel = (e) => {
    console.log("Scrolled", e);
  };

  const handleMouseMove = (e) => {
    if (e.buttons == 1) {
      // Left mouse button held
      setX(x - e.movementX);
      setY(y - e.movementY);
    }
  };

  return (
    <SVGViewer style={{ width: "100%", height: "100%" }}>
      <rect x={100} y={100} width={400} height={200} />
    </SVGViewer>
  );
};

export default Plan;
