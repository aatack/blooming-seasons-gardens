import Editor from "./editor/editor";
import Plan from "./plan/plan";
import {
  Modal,
  GardenSVG,
  Hovered,
  Selected,
  PlanX,
  PlanY,
  PlanScale,
} from "../model/context";
import { HorizontalSplit } from "./common/layout";
import { useEffect, useState } from "react";
import { useGarden, useLoaded } from "../model/selectors";
import ChooseGarden from "./loading/choose";
import { useDispatch } from "react-redux";
import { saveData } from "../storage";

const App = () => {
  const dispatch = useDispatch();

  const [gardenSVG, setGardenSVG] = useState(null);

  const garden = useGarden();
  const loaded = useLoaded();

  useEffect(() => {
    const interval = setInterval(() => {
      saveData();
    }, 60 * 1000);
    window.addEventListener("beforeunload", saveData);

    return () => {
      clearInterval(interval);
      window.removeEventListener("beforeunload", saveData);
    };
  }, []);

  useEffect(() => {
    fetch("/load")
      .then((response) => response.json())
      .then((data) => dispatch({ type: "initialised", payload: data.message }));
  }, []);

  return (
    <>
      <PlanScale.Provider value={useState(100)}>
        <PlanY.Provider value={useState(0)}>
          <PlanX.Provider value={useState(0)}>
            <Modal.Provider>
              <Selected.Provider>
                <Hovered.Provider>
                  <GardenSVG.Provider value={[gardenSVG, setGardenSVG]}>
                    <Modal.Component />
                    {!loaded ? (
                      <p>Loading saved data from disk...</p>
                    ) : garden === null ? (
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
              </Selected.Provider>
            </Modal.Provider>
          </PlanX.Provider>
        </PlanY.Provider>
      </PlanScale.Provider>
    </>
  );
};

export default App;
