import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";
import { addBed, removeBed, renameBed } from "../model/store";

const Editor = () => {
  const dispatch = useDispatch();

  const handleAddBed = () => {
    dispatch(addBed());
  };

  const garden = useSelector((state) => state.garden);
  return (
    <div style={{ backgroundColor: "lightGrey", padding: 8 }}>
      <button onClick={handleAddBed}>Add Bed</button>
      {garden.map((bed) => (
        <Bed bed={bed} key={bed.identifier} />
      ))}
    </div>
  );
};

const Bed = ({ bed }) => {
  const dispatch = useDispatch();

  const [hovered, setHovered] = useState(false);
  const [renaming, setRenaming] = useState(false);

  const handleRemoveBed = () => {
    dispatch(removeBed(bed.identifier));
  };

  const handleRenameStart = () => {
    setRenaming(true);
  };

  const handleRenameCancel = () => {
    setRenaming(false);
  };

  const handleRenameConfirm = () => {
    setRenaming(false);
    dispatch(renameBed(bed.identifier, bed.name + "."));
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
      {hovered && !renaming && (
        <button onClick={handleRenameStart}>Rename</button>
      )}
      {renaming && (
        <button onClick={handleRenameConfirm}>Confirm Rename</button>
      )}
      {renaming && <button onClick={handleRenameCancel}>Cancel Rename</button>}
    </div>
  );
};

export default Editor;
