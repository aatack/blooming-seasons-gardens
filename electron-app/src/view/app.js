import Editor from "./editor";
import { Modal, useModal } from "../model/context";
import { Popup } from "./common";

const App = () => {
  return (
    <Modal.Provider value={useModal()}>
      <Popup />
      <Editor />
    </Modal.Provider>
  );
};

export default App;
