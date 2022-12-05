import { useContext } from "react";
import { Modal } from "../model/context";
import { addPlantTemplate, addLabelTemplate } from "../model/actions";
import Template from "./editor/template";
import { useDispatch } from "react-redux";
import { Dropdown, space, TextBox } from "./common/input";
import { useState } from "react";
import { useNursery } from "../model/selectors";

const Nursery = () => {
  const templates = useNursery();
  console.log(templates);
  const modal = useContext(Modal);

  const handleAddTemplate = () => {
    modal.put(<CreateTemplateModal />);
  };

  const handleClose = () => {
    modal.pop();
  };

  return (
    <>
      <h1>Nursery</h1>
      <button onClick={handleAddTemplate}>Add Template</button>
      {templates.map((template) => (
        <Template template={template} key={template.identifier} />
      ))}

      <br />
      <button onClick={handleClose}>Close</button>
    </>
  );
};

export const CreateTemplateModal = () => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);

  const [type, setType] = useState("plant");
  const [name, setName] = useState("");

  const onDone = () => {
    switch (type) {
      case "plant":
        dispatch(addPlantTemplate(name));
        break;
      case "label":
        dispatch(addLabelTemplate(name));
        break;
      default:
        console.error(`Unknown template type: ${type}`);
    }

    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Create Template</h3>
      <Dropdown
        value={type}
        setValue={setType}
        options={[
          { name: "Plant", key: "plant", value: "plant" },
          { name: "Label", key: "label", value: "label" },
        ]}
      />
      <TextBox value={name} setValue={setName} />
      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Nursery;
