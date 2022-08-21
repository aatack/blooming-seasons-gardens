import { useContext } from "react";
import { useSelector } from "react-redux";
import { Modal } from "../../model/context";
import { addTemplate } from "../../model/store";
import Template from "./template";
import { useDispatch } from "react-redux";
import { TextBox } from "../common";
import { useState } from "react";

const Nursery = () => {
  const templates = useSelector((state) => state.nursery);
  const modal = useContext(Modal);

  const handleAddTemplate = () => {
    modal.set({ modal: <CreateTemplateModal /> });
  };

  return (
    <>
      <h1>Nursery</h1>
      <button onClick={handleAddTemplate}>Add Template</button>
      {templates.map((template) => (
        <Template template={template} key={template.identifier} />
      ))}
    </>
  );
};

const CreateTemplateModal = () => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const [name, setName] = useState("");

  const onDone = () => {
    dispatch(addTemplate(name));
    modal.set({ modal: <Nursery /> });
  };

  const onCancel = () => {
    modal.set({ modal: <Nursery /> });
  };

  return (
    <>
      <h3>Create Template</h3>
      <TextBox value={name} setValue={setName} />
      <button onClick={onDone}>Done</button>
      <button onClick={onCancel}>Cancel</button>
    </>
  );
};

export default Nursery;
