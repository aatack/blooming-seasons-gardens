import { useContext } from "react";
import { Modal } from "../model/context";
import { addTemplate } from "../model/actions";
import Template from "./editor/template";
import { useDispatch } from "react-redux";
import { space, TextBox } from "./common/input";
import { useState } from "react";
import { useNursery } from "../model/selectors";

const Nursery = () => {
  const templates = useNursery();
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
  const [name, setName] = useState("");

  const onDone = () => {
    dispatch(addTemplate(name));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Create Template</h3>
      <TextBox value={name} setValue={setName} />
      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Nursery;
