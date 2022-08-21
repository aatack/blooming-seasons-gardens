import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import { removeBed, renameBed } from "../../model/store";
import { TextBox } from "../common";
import { Modal } from "../../model/context";

const Bed = ({ bed }) => {
  const dispatch = useDispatch();

  const modal = useContext(Modal);
  const [hovered, setHovered] = useState(false);
  const [background, setBackground] = useState(null);

  const handleRemoveBed = () => {
    dispatch(removeBed(bed.identifier));
  };

  const handleRename = () => {
    modal.put(<RenameBedModal bed={bed} />);
  };

  const handleMouseEnter = () => {
    setHovered(true);
    setBackground("lightBlue");
  };

  const handleMouseLeave = () => {
    setHovered(false);
    setBackground(null);
  };

  return (
    <div
      className="bed-editor"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{ backgroundColor: background }}
    >
      <p style={{ display: "inline-block" }}>{bed.name}</p>

      {hovered && <button onClick={handleRemoveBed}>Remove</button>}
      {hovered && <button onClick={handleRename}>Rename</button>}
    </div>
  );
};

const RenameBedModal = ({ bed }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const [name, setName] = useState(bed.name);

  const onDone = () => {
    dispatch(renameBed(bed.identifier, name));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Rename Bed</h3>
      <TextBox value={name} setValue={setName} />
      <button onClick={onDone}>Done</button>
      <button onClick={onCancel}>Cancel</button>
    </>
  );
};

export default Bed;
