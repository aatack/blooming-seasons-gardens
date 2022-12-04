import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { space, TextBox, NumericTextBox, Dropdown } from "../common/input";
import { copyElement, editElement, removeElement } from "../../model/actions";
import { Hovered, Modal, Selected } from "../../model/context";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";

const Label = ({ label }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const hovered = useContext(Hovered);
  const selected = useContext(Selected);

  const handleMouseEnter = () => {
    hovered.set(label);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const handleClick = () => {
    selected.set(label);
  };

  const handleEdit = () => {
    modal.put(<EditLabelModal label={label} />);
  };

  const handleRemove = () => {
    dispatch(removeElement(label));
  };

  const handleCopy = () => {
    dispatch(copyElement(label));
  };

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
      style={{
        backgroundColor: hovered.matches(label)
          ? HOVERED_COLOUR
          : selected.matches(label)
          ? SELECTED_COLOUR
          : null,
      }}
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
      {hovered.matches(label) &&
        space(<button onClick={handleCopy}>Copy</button>)}
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
  const [font, setFont] = useState(label.font);

  const onDone = () => {
    dispatch(
      editElement(label, {
        text: text,
        position: { x: x, y: y },
        size: size,
        font: font,
      })
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
      <p>x =</p>
      <NumericTextBox value={x} setValue={setX} />
      <p>y =</p>
      <NumericTextBox value={y} setValue={setY} />
      <p>Size</p>
      <NumericTextBox value={size} setValue={setSize} />
      <p>Font</p>
      <Dropdown
        value={font}
        setValue={setFont}
        options={[
          { name: "Arial", key: "Arial", value: "Arial" },
          { name: "Spectral", key: "Spectral", value: "Spectral" },
        ]}
      />
      <br />
      <br />
      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Label;
