import Editor from "./editor/editor";
import Plan from "./plan/plan";
import { Modal } from "../model/context";
import { HorizontalSplit } from "./common/layout";

const App = () => {
  return (
    <Modal.Provider>
      <>
        <Modal.Component />
        <HorizontalSplit
          dragWidth={6}
          minimumWidth={100}
          initialWidth={window.innerWidth * 0.3}
        >
          <>
            <Editor />
            <Plan />
          </>
        </HorizontalSplit>
      </>
    </Modal.Provider>
  );
};

export default App;
