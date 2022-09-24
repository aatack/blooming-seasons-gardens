import { Modal } from "../model/context";
import { useContext } from "react";
import { loadGarden, saveGarden, listGardens, deleteGarden } from "../storage";
import { space } from "./common/input";
import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";
import defaultGarden from "../model/default";
import { RenameGardenModal } from "./editor/rename";

const ChangeGardenModal = () => {
  // TODO: re-render whenever the list of current gardens changes

  const gardens = listGardens();
  const garden = useSelector((state) => state);
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const handleNew = () => {
    saveGarden(garden);
    dispatch({ type: "loaded", payload: defaultGarden });
    modal.pop();
    modal.put(<RenameGardenModal garden={{ ...garden, path: null }} />);
  };

  const handleClose = () => {
    modal.pop();
  };

  return (
    <>
      <h1>Change Garden</h1>
      <button onClick={handleNew}>New</button>
      {gardens.map((path) => (
        <Garden path={path} key={path} />
      ))}

      <br />
      <button onClick={handleClose}>Close</button>
    </>
  );
};

const Garden = ({ path }) => {
  const dispatch = useDispatch();
  const currentGarden = useSelector((state) => state);

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

export default ChangeGardenModal;
