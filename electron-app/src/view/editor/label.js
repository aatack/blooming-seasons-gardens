import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { space, TextBox } from "../common";
import { editElement, removeElement } from "../../model/store";
import { Modal } from "../../model/context";

const Label = ({ label }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);

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
    modal.put(<EditLabelModal label={label} />);
  };

  const handleRemove = () => {
    dispatch(removeElement(label));
  };

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{ backgroundColor: background }}
    >
      <p style={{ display: "inline-block" }}>Label: {label.text}</p>

      {hovered && space(<button onClick={handleEdit}>Edit</button>)}
      {hovered && space(<button onClick={handleRemove}>Remove</button>)}
    </div>
  );
};

const EditLabelModal = ({ label }) => {
  const modal = useContext(Modal);
  const [text, setText] = useState(label.text);
  const dispatch = useDispatch();

  const onDone = () => {
    dispatch(editElement(label, { text: text }));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Edit Label</h3>

      <p>Text</p>
      <TextBox value={text} setValue={setText} />

      <br />
      <br />

      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Label;
