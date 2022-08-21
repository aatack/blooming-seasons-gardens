import { useState } from "react";
import { useTemplate } from "../../model/selectors";
import { space } from "../common";

const Plant = ({ plant }) => {
  const template = useTemplate(plant.template);

  const [hovered, setHovered] = useState(false);

  const handleEdit = () => {};

  const handleRemove = () => {};

  return (
    <div>
      <p style={{ display: "inline-block" }}>
        {template ? template.name : plant.name} (x = {plant.position.x}, y ={" "}
        {plant.position.y})
      </p>
      {space(<button onClick={handleEdit}>Edit</button>)}
      <button onClick={handleRemove}>Remove</button>
    </div>
  );
};

export default Plant;
