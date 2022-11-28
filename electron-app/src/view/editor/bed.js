import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import {
  addArrow,
  addCustomPlant,
  addLabel,
  addTemplatePlant,
  removeBed,
  renameBed,
} from "../../model/actions";
import { Checkbox, TextBox, Dropdown, space } from "../common/input";
import { Modal, Hovered, Selected } from "../../model/context";
import { CreateTemplateModal } from "../nursery";
import Plant from "./plant";
import Label from "./label";
import Arrow from "./arrow";
import { useNursery } from "../../model/selectors";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";

const Bed = ({ bed }) => {
  const dispatch = useDispatch();

  const modal = useContext(Modal);
  const hovered = useContext(Hovered);
  const selected = useContext(Selected);

  const handleRemoveBed = () => {
    dispatch(removeBed(bed));
  };

  const handleRename = () => {
    modal.put(<RenameBedModal bed={bed} />);
  };

  const handleAddPlant = () => {
    modal.put(<AddPlantModal bed={bed} />);
  };

  const handleAddLabel = () => {
    modal.put(<AddLabelModal bed={bed} />);
  };

  const handleAddArrow = () => {
    dispatch(addArrow(bed));
  };

  const handleMouseEnter = () => {
    hovered.set(bed);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const handleClick = () => {
    selected.set(bed);
  };

  const isHovered = hovered.matches(bed);
  const isSelected = selected.matches(bed);

  return (
    <>
      <div
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onClick={handleClick}
        style={{
          backgroundColor: isHovered
            ? HOVERED_COLOUR
            : isSelected
            ? SELECTED_COLOUR
            : null,
        }}
      >
        <p style={{ display: "inline-block" }}>{bed.name}</p>
        {isHovered && space(<button onClick={handleRemoveBed}>Remove</button>)}
        {isHovered && space(<button onClick={handleRename}>Rename</button>)}
        {isHovered &&
          space(<button onClick={handleAddPlant}>Add Plant</button>)}
        {isHovered &&
          space(<button onClick={handleAddLabel}>Add Label</button>)}
        {isHovered &&
          space(<button onClick={handleAddArrow}>Add Arrow</button>)}
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
      {space(<button onClick={onDone}>Done</button>)}
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

const AddPlantModal = ({ bed }) => {
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const templates = useNursery();

  const templatesAvailable = templates.length > 0;

  const [custom, setCustom] = useState(false);
  const [name, setName] = useState("");
  const [template, setTemplate] = useState(
    templatesAvailable ? templates[0] : null
  );

  const onDone = () => {
    if (custom) {
      dispatch(addCustomPlant(bed, name));
    } else {
      dispatch(addTemplatePlant(bed, template));
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
        <Dropdown
          options={templates.map((t) => ({
            key: t.identifier,
            value: t,
            name: t.name,
          }))}
          value={template}
          setValue={setTemplate}
        />
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
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

const AddLabelModal = ({ bed }) => {
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const [text, setText] = useState("");

  const onDone = () => {
    dispatch(addLabel(bed, text));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Add Label</h3>

      <p>Text</p>
      <TextBox value={text} setValue={setText} />

      <br />
      <br />

      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

const renderElement = (element) => {
  switch (element.type) {
    case "plant":
      return <Plant key={element.identifier} plant={element} />;
    case "label":
      return <Label key={element.identifier} label={element} />;
    case "arrow":
      return <Arrow key={element.identifier} arrow={element} />;
    default:
      console.warn(
        "Cannot render element with the following type:",
        element.type
      );
      return null;
  }
};

export default Bed;
