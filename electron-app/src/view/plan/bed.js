import Plant from "./plant";
import Label from "./label";
import Arrow from "./arrow";
import { Translate } from "../common/rendering";

const Bed = ({ bed }) => {
  return (
    <Translate x={bed.x || 0} y={bed.y || 0}>
      {bed.elements.map(renderElement)}
    </Translate>
  );
};

const renderElement = (element) => {
  switch (element.type) {
    case "plant":
      return <Plant key={element.identifier} plant={element} />;
    case "label":
      return <Label key={element.identifier} label={element} />;
    case "arrow":
      return <Arrow key={element.identifier} arrow={element} />;
    default:
      console.warn(
        "Cannot render element with the following type:",
        element.type
      );
      return null;
  }
};

export default Bed;
