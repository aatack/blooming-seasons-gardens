import { Modal } from "../../model/context";
import { useContext } from "react";
import {
  loadGarden,
  saveGarden,
  listGardens,
  deleteGarden,
} from "../../storage";
import { space } from "../common/input";
import { useDispatch } from "react-redux";
import { useState } from "react";
import defaultGarden from "../../model/default";
import { NewGardenModal } from "./new";
import { useGarden, useGardens } from "../../model/selectors";

const ChooseGarden = () => {
  // TODO: re-render whenever the list of current gardens changes

  const gardens = useGardens();
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const handleNew = () => {
    console.log("Putting modal");
    modal.put(<NewGardenModal />);
  };

  return (
    <>
      <h1>Choose Garden</h1>
      <br />
      <button onClick={handleNew}>New</button>
      <br />
      {gardens.map((garden) => (
        <Garden path={garden.path} key={garden.workspaceIdentifier} />
      ))}
    </>
  );
};

const Garden = ({ path }) => {
  const dispatch = useDispatch();
  const currentGarden = useGarden();

  const modal = useContext(Modal);
  const [hovered, setHovered] = useState(false);

  const handleLoad = () => {
    // TODO: warn before loading over an unsaved garden
    saveGarden(currentGarden);
    dispatch({ type: "loaded", payload: loadGarden(path) });
    modal.pop();
  };

  const handleCopy = () => {
    const gardens = listGardens();

    var index = 1;
    var attempt = `${path} (copy ${index})`;
    while (gardens.indexOf(attempt) !== -1) {
      index++;
      attempt = `${path} (copy ${index})`;
    }

    const gg = { ...currentGarden, path: attempt };
    saveGarden(gg);
  };

  const handleDelete = () => {
    deleteGarden(path);
  };

  const handleMouseEnter = () => {
    setHovered(true);
  };

  const handleMouseLeave = () => {
    setHovered(false);
  };

  return (
    <div onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
      <p style={{ display: "inline-block" }}>{path}</p>

      {hovered && space(<button onClick={handleLoad}>Load</button>)}
      {hovered && space(<button onClick={handleCopy}>Copy</button>)}
      {hovered && space(<button onClick={handleDelete}>Delete</button>)}
    </div>
  );
};

export default ChooseGarden;
