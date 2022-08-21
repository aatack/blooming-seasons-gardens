import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import { removeBed, renameBed } from "../../model/store";
import { TextBox } from "../common";
import { Modal } from "../../model/context";

const Bed = ({ bed }) => {
  const dispatch = useDispatch();

  const [_, setModal] = useContext(Modal);
  const [hovered, setHovered] = useState(false);

  const handleRemoveBed = () => {
    dispatch(removeBed(bed.identifier));
  };

  const handleRename = () => {
    setModal({
      modal: <RenameBedModal bed={bed} />,
    });
  };

  const handleMouseEnter = () => {
    setHovered(true);
  };

  const handleMouseLeave = () => {
    setHovered(false);
  };

  return (
    <div onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
      <p style={{ display: "inline-block" }}>{bed.name}</p>

      {hovered && <button onClick={handleRemoveBed}>Remove</button>}
      {hovered && <button onClick={handleRename}>Rename</button>}
    </div>
  );
};

const RenameBedModal = ({ bed }) => {
  const dispatch = useDispatch();
  const [_, setModal] = useContext(Modal);
  const [name, setName] = useState(bed.name);

  const onDone = () => {
    dispatch(renameBed(bed.identifier, name));
    setModal();
  };

  const onCancel = () => {
    setModal();
  };

  return (
    <>
      <p>Rename Bed</p>
      <TextBox value={name} onChange={setName} />
      <button onClick={onDone}>Done</button>
      <button onClick={onCancel}>Cancel</button>
    </>
  );
};

export default Bed;
