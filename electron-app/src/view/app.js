import Editor from "./editor";
import { Modal } from "../model/context";
import { Popup } from "./common";

const App = () => {
  return (
    <Modal.Provider>
      <>
        <Popup />
        <Editor />
      </>
    </Modal.Provider>
  );
};

export default App;
