import Editor from "./editor/editor";
import Plan from "./plan/plan";
import { Modal } from "../model/context";

const App = () => {
  return (
    <Modal.Provider>
      <>
        <Modal.Component />
        <div>
          <div
            style={{
              position: "fixed",
              height: "100%",
              left: "0%",
              width: "30%",
              top: "0%",
            }}
          >
            <Editor />
          </div>
          <div
            style={{
              position: "fixed",
              height: "100%",
              left: "30%",
              right: "0%",
              top: 0,
            }}
          >
            <Plan />
          </div>
          <div
            style={{
              position: "fixed",
              height: "100%",
              left: "30%",
              width: "1%",
              top: 0,
              backgroundColor: "blue",
            }}
          ></div>
        </div>
      </>
    </Modal.Provider>
  );
};

export default App;
