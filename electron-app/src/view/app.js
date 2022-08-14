import Editor from "./editor/editor";
import { Modal } from "../model/context";

const App = () => {
  return (
    <Modal.Provider>
      <>
        <Modal.Component />
        <Editor />
      </>
    </Modal.Provider>
  );
};

export default App;
