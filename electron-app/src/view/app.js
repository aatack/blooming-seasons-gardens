import Editor from "./editor/editor";
import Plan from "./plan/plan";
import { Modal, GardenSVG, Hovered } from "../model/context";
import { HorizontalSplit } from "./common/layout";
import { useEffect, useState } from "react";
import { useGarden } from "../model/selectors";
import ChooseGarden from "./loading/choose";
import { storeData } from "../model/store";

const App = () => {
  const [gardenSVG, setGardenSVG] = useState(null);

  const garden = useGarden();

  const handleClose = () => {
    storeData();
  };

  useEffect(() => {
    const interval = setInterval(() => {
      storeData();
    }, 60 * 1000);
    window.addEventListener("beforeunload", handleClose);

    return () => {
      clearInterval(interval);
      window.removeEventListener("beforeunload", handleClose);
    };
  }, []);

  return (
    <>
      <Modal.Provider>
        <Hovered.Provider>
          <GardenSVG.Provider value={[gardenSVG, setGardenSVG]}>
            <Modal.Component />
            {garden === null ? (
              <ChooseGarden />
            ) : (
              <>
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
