import Editor from "./editor/editor";
import Plan from "./plan/plan";
import { Modal, GardenSVG, Hovered } from "../model/context";
import { HorizontalSplit } from "./common/layout";
import { useEffect, useState } from "react";
import { useGarden, useLoaded } from "../model/selectors";
import ChooseGarden from "./loading/choose";
import { store, storeData } from "../model/store";
import { useDispatch } from "react-redux";

const saveData = () => {
  (async () => {
    // TODO: clear the state's history
    const state = store.getState();
    if (!state.garden) {
      console.error("Potentially saving empty data")
    }

    const rawResponse = await fetch("/save", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(state),
    });

    const status = await rawResponse.json();
    if (status !== 200) {
      console.error("Error saving to disk");
    }
  })();
};

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
