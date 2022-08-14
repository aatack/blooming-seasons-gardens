import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";
import { addBed, removeBed, renameBed } from "../model/store";

const App = () => {
  return (
    <>
      <AddBed />
      <Garden />
    </>
  );
};

const AddBed = () => {
  const dispatch = useDispatch();
  const handleClick = () => {
    dispatch(addBed());
  };

  return <button onClick={handleClick}>Add Bed</button>;
};

const Garden = () => {
  const garden = useSelector((state) => state.garden);
  return garden.map((bed) => <Bed bed={bed} key={bed.identifier} />);
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
