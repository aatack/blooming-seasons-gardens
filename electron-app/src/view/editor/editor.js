import { useContext } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addBed } from "../../model/store";
import { TextBox } from "../common";
import { Modal } from "../../model/context";
import { useState } from "react";
import Bed from "./bed";

const Editor = () => {
  const [_, setModal] = useContext(Modal);

  const handleAddBed = () => {
    setModal({ modal: <CreateBedModal /> });
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

export default Editor;

const CreateBedModal = () => {
  const dispatch = useDispatch();
  const [_, setModal] = useContext(Modal);
  const [name, setName] = useState("");

  const onDone = () => {
    dispatch(addBed(name));
    setModal();
  };

  const onCancel = () => {
    setModal();
  };

  return (
    <>
      <p>Create Bed</p>
      <TextBox value={name} onChange={setName} />
      <button onClick={onDone}>Done</button>
      <button onClick={onCancel}>Cancel</button>
    </>
  );
};
