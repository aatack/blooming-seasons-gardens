import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { space, TextBox, NumericTextBox } from "../common/input";
import { editElement, removeElement } from "../../model/store";
import { Hovered, Modal } from "../../model/context";

const Label = ({ label }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const hovered = useContext(Hovered);

  const [background, setBackground] = useState(null);

  const handleMouseEnter = () => {
    hovered.set(label);
    setBackground("lightBlue");
  };

  const handleMouseLeave = () => {
    hovered.set(null);
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
      {space(
        <p style={{ display: "inline-block" }}>
          (x = {label.position.x}, y = {label.position.y})
        </p>
      )}

      {hovered.matches(label) &&
        space(<button onClick={handleEdit}>Edit</button>)}
      {hovered.matches(label) &&
        space(<button onClick={handleRemove}>Remove</button>)}
    </div>
  );
};

const EditLabelModal = ({ label }) => {
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const [text, setText] = useState(label.text);
  const [x, setX] = useState(label.position.x);
  const [y, setY] = useState(label.position.y);
  const [size, setSize] = useState(label.size);

  const onDone = () => {
    dispatch(
      editElement(label, { text: text, position: { x: x, y: y }, size: size })
    );
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
      <p>Position</p>
      x = <NumericTextBox value={x} setValue={setX} />, y ={" "}
      <NumericTextBox value={y} setValue={setY} />
      <p>Size</p>
      <NumericTextBox value={size} setValue={setSize} />
      <br />
      <br />
      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Label;
