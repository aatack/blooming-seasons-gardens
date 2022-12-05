import Plant from "./plant";
import Label from "./label";
import Arrow from "./arrow";
import { Translate } from "../common/rendering";
import { expandTemplate, useNursery } from "../../model/selectors";

const Bed = ({ bed }) => {
  const nursery = useNursery();
  const elements = bed.elements.map((element) =>
    expandTemplate(element, nursery)
  );

  return (
    <Translate x={bed.x || 0} y={bed.y || 0}>
      {elements.map(renderElement)}
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
