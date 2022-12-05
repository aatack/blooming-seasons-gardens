import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import {
  addArrow,
  addCustomPlant,
  addCustomLabel,
  addTemplateLabel,
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
import { useNursery, expandTemplate } from "../../model/selectors";
import { HOVERED_COLOUR, SELECTED_COLOUR } from "../../constants";

const Bed = ({ bed }) => {
  const dispatch = useDispatch();
  const nursery = useNursery();

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

  const elements = bed.elements
    .map((element) => expandTemplate(element, nursery))
    .sort((left, right) => {
      const stats = (element) => {
        return {
          name:
            element.type === "plant"
              ? element.name
              : element.type === "label"
              ? element.text
              : "_" + element.type,
          position:
            element.type === "arrow" ? element.start.x : element.position.x,
        };
      };

      const leftStats = stats(left);
      const rightStats = stats(right);

      if (leftStats.name === rightStats.name) {
        if (leftStats.position === rightStats.name) {
          return left.identifier < right.identifier ? -1 : 1;
        } else {
          return leftStats.position < rightStats.position ? -1 : 1;
        }
      } else {
        return leftStats.name < rightStats.name ? -1 : 1;
      }
    });

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

      <div style={{ marginLeft: "20px" }}>{elements.map(renderElement)}</div>
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

  const templates = useNursery().filter(
    (template) => template.type === "plant"
  );

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

  const templates = useNursery().filter(
    (template) => template.type === "label"
  );

  const templatesAvailable = templates.length > 0;

  const [custom, setCustom] = useState(false);
  const [text, setText] = useState("");
  const [template, setTemplate] = useState(
    templatesAvailable ? templates[0] : null
  );

  const onDone = () => {
    if (custom) {
      dispatch(addCustomLabel(bed, text));
    } else {
      dispatch(addTemplateLabel(bed, template));
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

      {custom && <TextBox value={text} setValue={setText} />}
      {!custom && templatesAvailable && (
        <Dropdown
          options={templates.map((t) => ({
            key: t.identifier,
            value: t,
            name: t.text,
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
