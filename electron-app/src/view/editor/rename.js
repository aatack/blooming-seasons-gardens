import { Modal } from "../../model/context";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { TextBox, space } from "../common/input";
import { useContext } from "react";
import { renameGarden } from "../../model/actions";

export const RenameGardenModal = ({ garden }) => {
  const [path, setPath] = useState(garden.path || "");
  const dispatch = useDispatch();
  const modal = useContext(Modal);

  const onDone = () => {
    dispatch(renameGarden(path));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>{garden.path ? "Rename" : "Name"} Garden</h3>

      <TextBox value={path} setValue={setPath} />

      <br />
      <br />

      {space(
        <button onClick={onDone} disabled={!path}>
          Done
        </button>
      )}
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};
