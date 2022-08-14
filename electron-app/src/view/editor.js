import { useDispatch, useSelector } from "react-redux";
import { useContext, useState } from "react";
import { addBed, removeBed, renameBed } from "../model/store";
import { Modal } from "../model/context";

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

  const [_, setModal] = useContext(Modal.Context);
  const [hovered, setHovered] = useState(false);

  const handleRemoveBed = () => {
    dispatch(removeBed(bed.identifier));
  };

  const handleRename = () => {
    setModal({
      element: <p>Rename bed {bed.identifier}</p>,
      onClose: () => {
        console.log("Closing rename window for bed", bed.identifier);
      },
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

export default Editor;
