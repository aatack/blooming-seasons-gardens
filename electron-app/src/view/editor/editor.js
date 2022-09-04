import { useContext } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addBed } from "../../model/store";
import { space, TextBox } from "../common/input";
import { Modal } from "../../model/context";
import { useState } from "react";
import Nursery from "./nursery";
import Bed from "./bed";

const Editor = () => {
  const modal = useContext(Modal);

  const handleAddBed = () => {
    modal.put(<CreateBedModal />);
  };

  const handleViewNursery = () => {
    modal.put(<Nursery />);
  };

  const garden = useSelector((state) => state.garden);
  return (
    <div
      style={{
        backgroundColor: "lightGrey",
        padding: "8px -8px 8px 8px",
        width: "100%",
        height: "100%",
      }}
    >
      <button onClick={handleAddBed}>Add Bed</button>
      {space(<button onClick={handleViewNursery}>View Nursery</button>)}
      {garden.map((bed) => (
        <Bed bed={bed} key={bed.identifier} />
      ))}
    </div>
  );
};

const CreateBedModal = () => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const [name, setName] = useState("");

  const onDone = () => {
    dispatch(addBed(name));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Create Bed</h3>
      <TextBox value={name} setValue={setName} />
      {space(<button onClick={onDone}>Done</button>)}
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Editor;
