import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import { editTemplate, removeTemplate } from "../../model/store";
import { Modal } from "../../model/context";
import { NumberBox, TextBox } from "../common";

const Template = ({ template }) => {
  const dispatch = useDispatch();

  const modal = useContext(Modal);
  const [hovered, setHovered] = useState(false);

  const handleRemoveTemplate = () => {
    dispatch(removeTemplate(template.identifier));
  };

  const handleEdit = () => {
    modal.set(<EditTemplateModal template={template} />);
  };

  const handleMouseEnter = () => {
    setHovered(true);
  };

  const handleMouseLeave = () => {
    setHovered(false);
  };

  return (
    <div onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
      <p style={{ display: "inline-block" }}>{template.name}</p>

      {hovered && <button onClick={handleRemoveTemplate}>Remove</button>}
      {hovered && <button onClick={handleEdit}>Edit</button>}
    </div>
  );
};

const EditTemplateModal = ({ template }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);

  const [name, setName] = useState(template.name);
  const [size, setSize] = useState(template.size);
  const [colour, setColour] = useState(template.colour);

  const onDone = () => {
    dispatch(editTemplate(template.identifier, name, size, colour));
    modal.set();
  };

  const onCancel = () => {
    modal.set(); // TODO: enable modals to go back
  };

  return (
    <>
      <h3>Edit Template</h3>

      <p>Name</p>
      <TextBox value={name} setValue={setName} />

      <p>Size</p>
      <NumberBox value={size} setValue={setSize} />

      <p>Colour</p>
      <TextBox value={colour} setValue={setColour} />

      <p />
      <button onClick={onDone}>Done</button>
      <button onClick={onCancel}>Cancel</button>
    </>
  );
};

export default Template;
