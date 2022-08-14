import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";
import { addBed, removeBed, renameBed } from "../model/store";

const App = () => {
  return <Garden />;
};

const Garden = () => {
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

  const handleRemoveClick = () => {
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
      <button
        style={{ display: hovered ? "inline-block" : "none" }}
        onClick={handleRemoveClick}
      >
        Remove
      </button>
      <button
        style={{ display: hovered & !renaming ? "inline-block" : "none" }}
        onClick={handleRenameStart}
      >
        Rename
      </button>
      <button
        style={{ display: renaming ? "inline-block" : "none" }}
        onClick={handleRenameConfirm}
      >
        Confirm Rename
      </button>
      <button
        style={{ display: renaming ? "inline-block" : "none" }}
        onClick={handleRenameCancel}
      >
        Cancel Rename
      </button>
    </div>
  );
};

export default App;
