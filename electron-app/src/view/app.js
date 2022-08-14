import { useState } from "react";
import Editor from "./editor";
import { Modal } from "../model/context";
import { Popup } from "./common";

const App = () => {
  const [modal, setModal] = useState(null);

  return (
    <Modal.Provider value={[modal, setModal]}>
      <Popup />
      <Editor />
    </Modal.Provider>
  );
};

export default App;
