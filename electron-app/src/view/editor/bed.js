import { useDispatch, useSelector } from "react-redux";
import { useContext, useState } from "react";
import {
  addCustomPlant,
  addTemplatePlant,
  removeBed,
  renameBed,
} from "../../model/store";
import { Checkbox, TextBox, Dropdown } from "../common";
import { Modal } from "../../model/context";
import { CreateTemplateModal } from "./nursery";
import Plant from "./plant";

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
    <>
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

      <div style={{ marginLeft: "20px" }}>
        {bed.elements.map(renderElement)}
      </div>
    </>
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

  const templates = useSelector((state) => state.nursery);

  const templatesAvailable = templates.length > 0;

  const [custom, setCustom] = useState(false);
  const [name, setName] = useState("");
  const [template, setTemplate] = useState(
    templatesAvailable ? templates[0] : null
  );

  const onDone = () => {
    if (custom) {
      addCustomPlant(bed, name);
    } else {
      addTemplatePlant(bed, template);
    }

    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  const createTemplate = () => {
    modal.put(<CreateTemplateModal />);
  };

  return (
    <>
      <h3>Add Plant</h3>
      <p>Use template?</p>
      <Checkbox value={custom} setValue={setCustom} />

      {custom && <TextBox value={name} setValue={setName} />}
      {!custom && templatesAvailable && (
        <Dropdown options={templates} value={template} setValue={setTemplate} />
      )}
      {!custom && !templatesAvailable && (
        <>
          <p>No template available.</p>
          <button onClick={createTemplate}>Create template</button>
        </>
      )}

      <br />
      <br />

      <button onClick={onDone} disabled={!custom && !templatesAvailable}>
        Done
      </button>
      <button onClick={onCancel}>Cancel</button>
    </>
  );
};

const renderElement = (element) => {
  switch (element.type) {
    case "plant":
      return <Plant key={element.identifier} plant={element} />;
    default:
      console.warning(
        "Cannot render element with the following type:",
        element.type
      );
      return null;
  }
};

export default Bed;
