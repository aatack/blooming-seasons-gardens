import Editor from "./editor/editor";
import Plan from "./plan/plan";
import { Modal, GardenSVG, Hovered } from "../model/context";
import { HorizontalSplit } from "./common/layout";
import { useState } from "react";
import { useGarden } from "../model/selectors";
import LoadGardenModal from "./loading";

const App = () => {
  const [gardenSVG, setGardenSVG] = useState(null);

  const garden = useGarden();

  return (
    <>
      <Modal.Provider>
        <Hovered.Provider>
          <GardenSVG.Provider value={[gardenSVG, setGardenSVG]}>
            {garden === null ? (
              <LoadGardenModal />
            ) : (
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
            )}
          </GardenSVG.Provider>
        </Hovered.Provider>
      </Modal.Provider>
    </>
  );
};

export default App;
