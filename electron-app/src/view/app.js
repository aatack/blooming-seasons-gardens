import Editor from "./editor/editor";
import Plan from "./plan/plan";
import { Modal, GardenSVG, Hovered } from "../model/context";
import { HorizontalSplit } from "./common/layout";
import { useEffect, useState } from "react";
import { useGarden, useLoaded } from "../model/selectors";
import ChooseGarden from "./loading/choose";
import { storeData } from "../model/store";
import { useDispatch } from "react-redux";

const App = () => {
  const dispatch = useDispatch();

  const [gardenSVG, setGardenSVG] = useState(null);

  const garden = useGarden();
  const loaded = useLoaded();

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

  useEffect(() => {
    fetch("/load-data")
      .then((response) => response.json())
      .then((data) => dispatch({ type: "initialised", payload: data.message }));
  }, []);

  return (
    <>
      <Modal.Provider>
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
      </Modal.Provider>
    </>
  );
};

export default App;
