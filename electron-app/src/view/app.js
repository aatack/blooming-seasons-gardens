import Editor from "./editor/editor";
import Plan from "./plan/plan";
import { Modal, GardenSVG, Hovered } from "../model/context";
import { HorizontalSplit } from "./common/layout";
import { useState } from "react";

const App = () => {
  const [gardenSVG, setGardenSVG] = useState(null);

  return (
    <Modal.Provider>
      <Hovered.Provider>
        <GardenSVG.Provider value={[gardenSVG, setGardenSVG]}>
          <>
            <Modal.Component />
            <HorizontalSplit
              dragWidth={8}
              minimumWidth={100}
              initialWidth={window.innerWidth * 0.3}
              toggleKey={32} // Space bar
            >
              <>
                <Editor />
                <Plan />
              </>
            </HorizontalSplit>
          </>
        </GardenSVG.Provider>
      </Hovered.Provider>
    </Modal.Provider>
  );
};

export default App;
