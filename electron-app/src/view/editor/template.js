import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import { editTemplate, removeTemplate } from "../../model/store";
import { Modal } from "../../model/context";
import { ColourPicker, NumericTextBox, space, TextBox } from "../common/input";

const Template = ({ template }) => {
  const dispatch = useDispatch();

  const modal = useContext(Modal);
  const [hovered, setHovered] = useState(false);

  const handleRemoveTemplate = () => {
    dispatch(removeTemplate(template));
  };

  const handleEdit = () => {
    modal.put(<EditTemplateModal template={template} />);
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

      {hovered && space(<button onClick={handleRemoveTemplate}>Remove</button>)}
      {hovered && space(<button onClick={handleEdit}>Edit</button>)}
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
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Edit Template</h3>

      <p>Name</p>
      <TextBox value={name} setValue={setName} />

      <p>Size</p>
      <NumericTextBox value={size} setValue={setSize} />

      <p>Colour</p>
      <ColourPicker value={colour} setValue={setColour} />

      <br />
      <br />

      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Template;
