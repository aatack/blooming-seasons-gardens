import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { useTemplate } from "../../model/selectors";
import { ColourPicker, NumericTextBox, space, TextBox } from "../common";
import { removeElement } from "../../model/store";
import { Modal } from "../../model/context";

const Plant = ({ plant }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);

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

  const handleEdit = () => {
    modal.put(<EditPlantModal plant={plant} />);
  };

  const handleRemove = () => {
    dispatch(removeElement(plant));
  };

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

const EditPlantModal = ({ plant }) => {
  const modal = useContext(Modal);

  const [name, setName] = useState(plant.name);
  const [x, setX] = useState(plant.position.x);
  const [y, setY] = useState(plant.position.y);
  const [size, setSize] = useState(plant.size);
  const [colour, setColour] = useState(plant.colour);

  const handleDone = () => {
    // TODO: dispatch the changes
    modal.pop();
  };

  const handleCancel = () => {
    modal.pop();
  };

  // TODO: handle the case where the plant is derived from a template

  return (
    <>
      <h3>Edit Plant</h3>
      <p>Name</p>
      <TextBox value={name} setValue={setName} />
      <p>Position</p>
      x = <NumericTextBox value={x} setValue={setX} />, y ={" "}
      <NumericTextBox value={y} setValue={setY} />
      <p>Size</p>
      <NumericTextBox value={size} setValue={setSize} />
      <p>Colour</p>
      <ColourPicker value={colour} setValue={setColour} />
      <br />
      <br />
      <button onClick={handleDone}>Done</button>
      {space(<button onClick={handleCancel}>Cancel</button>)}
    </>
  );
};

export default Plant;
