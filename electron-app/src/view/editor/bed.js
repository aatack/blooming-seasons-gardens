import { useDispatch, useSelector } from "react-redux";
import { useContext, useState } from "react";
import { removeBed, renameBed } from "../../model/store";
import { Checkbox, TextBox, Dropdown } from "../common";
import { Modal } from "../../model/context";

const Bed = ({ bed }) => {
  const dispatch = useDispatch();

  const modal = useContext(Modal);
  const [hovered, setHovered] = useState(false);
  const [background, setBackground] = useState(null);

  const handleRemoveBed = () => {
    dispatch(removeBed(bed));
  };

  const handleRename = () => {
    modal.put(<RenameBedModal bed={bed} />);
  };

  const handleAddPlant = () => {
    modal.put(<AddPlantModal bed={bed} />);
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
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{ backgroundColor: background }}
    >
      <p style={{ display: "inline-block" }}>{bed.name}</p>

      {hovered && <button onClick={handleRemoveBed}>Remove</button>}
      {hovered && <button onClick={handleRename}>Rename</button>}
      {hovered && <button onClick={handleAddPlant}>Add Plant</button>}
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

const AddPlantModal = ({ bed }) => {
  const modal = useContext(Modal);

  // const templates = useSelector((state) => state.nursery);
  const templates = [
    { name: "Daffodil", identifier: 6 },
    { name: "Birch", identifier: 156 },
    { name: "Acer", identifier: 2 },
  ];

  const [custom, setCustom] = useState(false);
  const [name, setName] = useState("");
  const [template, setTemplate] = useState(templates[1]);

  const onDone = () => {
    // TODO: dispatch
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Add Plant</h3>
      <p>Use template?</p>
      <Checkbox value={custom} setValue={setCustom} />
      {custom && <TextBox value={name} setValue={setName} />}
      {!custom && (
        <Dropdown options={templates} value={template} setValue={setTemplate} />
      )}

      <br />
      <br />

      <button onClick={onDone}>Done</button>
      <button onClick={onCancel}>Cancel</button>
    </>
  );
};

export default Bed;
