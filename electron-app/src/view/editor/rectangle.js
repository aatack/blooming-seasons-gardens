import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { space, NumericTextBox, ColourPicker } from "../common/input";
import { copyElement, editElement, removeElement } from "../../model/actions";
import { Hovered, Modal, Selected } from "../../model/context";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";

const Rectangle = ({ rectangle }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const hovered = useContext(Hovered);
  const selected = useContext(Selected);

  const handleMouseEnter = () => {
    hovered.set(rectangle);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const handleClick = () => {
    selected.set(rectangle);
  };

  const handleEdit = () => {
    modal.put(<EditRectangleModal rectangle={rectangle} />);
  };

  const handleRemove = () => {
    dispatch(removeElement(rectangle));
  };

  const handleCopy = () => {
    dispatch(copyElement(rectangle));
  };

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
      style={{
        backgroundColor: hovered.matches(rectangle)
          ? HOVERED_COLOUR
          : selected.matches(rectangle)
          ? SELECTED_COLOUR
          : null,
      }}
    >
      <p style={{ display: "inline-block" }}>Rectangle</p>

      {hovered.matches(rectangle) &&
        space(<button onClick={handleEdit}>Edit</button>)}
      {hovered.matches(rectangle) &&
        space(<button onClick={handleRemove}>Remove</button>)}
      {hovered.matches(rectangle) &&
        space(<button onClick={handleCopy}>Copy</button>)}
    </div>
  );
};

const EditRectangleModal = ({ rectangle }) => {
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const [x, setX] = useState(rectangle.position.x);
  const [y, setY] = useState(rectangle.position.y);

  const [width, setWidth] = useState(rectangle.size.width);
  const [height, setHeight] = useState(rectangle.size.height);

  const [colour, setColour] = useState(rectangle.colour);

  const onDone = () => {
    dispatch(
      editElement(rectangle, {
        position: { x: x, y: y },
        size: { width: width, height: height },
        colour: colour,
      })
    );
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Edit Rectangle</h3>
      <p>Position</p>
      <p>x = </p>
      <NumericTextBox value={x} setValue={setX} />
      <p>y = </p>
      <NumericTextBox value={y} setValue={setY} />
      <p>Size</p>
      <p>Width = </p>
      <NumericTextBox value={width} setValue={setWidth} />
      <p>Height =</p>
      <NumericTextBox value={height} setValue={setHeight} />
      <p>Colour</p>
      <ColourPicker value={colour} setValue={setColour} />
      <br />
      <br />
      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Rectangle;
