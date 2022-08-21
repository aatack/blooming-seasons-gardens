import { useState } from "react";
import { useTemplate } from "../../model/selectors";
import { space } from "../common";

const Plant = ({ plant }) => {
  const template = useTemplate(plant.template);

  const [hovered, setHovered] = useState(false);
  const [background, setBackground] = useState(null);

  const handleMouseEnter = () => {
    setHovered(true);
    setBackground("lightBlue");
  };

  const handleMouseLeave = () => {
    setHovered(false);
    setBackground(null);
  };

  const handleEdit = () => {};

  const handleRemove = () => {};

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{ backgroundColor: background }}
    >
      <p style={{ display: "inline-block" }}>
        {template ? template.name : plant.name}
      </p>
      {space(
        <p style={{ display: "inline-block" }}>
          (x = {plant.position.x}, y = {plant.position.y})
        </p>
      )}

      {hovered && space(<button onClick={handleEdit}>Edit</button>)}
      {hovered && space(<button onClick={handleRemove}>Remove</button>)}
    </div>
  );
};

export default Plant;
