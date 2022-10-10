import { Modal } from "../../model/context";
import { useContext } from "react";
import { space } from "../common/input";
import { useDispatch } from "react-redux";
import { useState } from "react";
import { NewGardenModal } from "./new";
import { useGardens } from "../../model/selectors";
import {
  workspaceCopied,
  workspaceDeleted,
  workspacePulled,
} from "../../model/actions";

const ChooseGarden = () => {
  // TODO: re-render whenever the list of current gardens changes

  const gardens = useGardens();
  const modal = useContext(Modal);

  const handleNew = () => {
    modal.put(<NewGardenModal />);
  };

  return (
    <>
      <h1>Choose Garden</h1>
      <br />
      <button onClick={handleNew}>New</button>
      <br />
      {gardens.map((garden) => (
        <Garden
          path={garden.path}
          identifier={garden.workspaceIdentifier}
          key={garden.workspaceIdentifier}
        />
      ))}
    </>
  );
};

const Garden = ({ path, identifier }) => {
  const dispatch = useDispatch();

  const modal = useContext(Modal);
  const [hovered, setHovered] = useState(false);

  const handleLoad = () => {
    dispatch(workspacePulled(identifier));
    modal.pop();
  };

  const handleCopy = () => {
    dispatch(workspaceCopied(identifier));
  };

  const handleDelete = () => {
    // TODO: confirm with the user before deleting
    dispatch(workspaceDeleted(identifier));
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
