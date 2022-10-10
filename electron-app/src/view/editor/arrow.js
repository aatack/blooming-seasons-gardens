import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { space, NumericTextBox } from "../common/input";
import { copyElement, editElement, removeElement } from "../../model/actions";
import { Hovered, Modal } from "../../model/context";

const Arrow = ({ arrow }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const hovered = useContext(Hovered);

  const handleMouseEnter = () => {
    hovered.set(arrow);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const handleEdit = () => {
    modal.put(<EditArrowModal arrow={arrow} />);
  };

  const handleRemove = () => {
    dispatch(removeElement(arrow));
  };

  const handleCopy = () => {
    dispatch(copyElement(arrow));
  };

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{ backgroundColor: hovered.matches(arrow) ? "lightBlue" : null }}
    >
      <p style={{ display: "inline-block" }}>Arrow</p>

      {hovered.matches(arrow) &&
        space(<button onClick={handleEdit}>Edit</button>)}
      {hovered.matches(arrow) &&
        space(<button onClick={handleRemove}>Remove</button>)}
      {hovered.matches(arrow) &&
        space(<button onClick={handleCopy}>Copy</button>)}
    </div>
  );
};

const EditArrowModal = ({ arrow }) => {
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const [startX, setStartX] = useState(arrow.start.x);
  const [startY, setStartY] = useState(arrow.start.y);

  const [endX, setEndX] = useState(arrow.end.x);
  const [endY, setEndY] = useState(arrow.end.y);

  const [width, setWidth] = useState(arrow.width);

  const onDone = () => {
    dispatch(
      editElement(arrow, {
        start: { x: startX, y: startY },
        end: { x: endX, y: endY },
        width: width,
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
      <p>Start</p>
      x = <NumericTextBox value={startX} setValue={setStartX} />, y ={" "}
      <NumericTextBox value={startY} setValue={setStartY} />
      <p>End</p>
      x = <NumericTextBox value={endX} setValue={setEndX} />, y ={" "}
      <NumericTextBox value={endY} setValue={setEndY} />
      <p>Width</p>
      <NumericTextBox value={width} setValue={setWidth} />
      <br />
      <br />
      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Arrow;
