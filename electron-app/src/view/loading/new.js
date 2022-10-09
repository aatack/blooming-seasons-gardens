import { Modal } from "../../model/context";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { TextBox, space } from "../common/input";
import { useContext } from "react";

export const NewGardenModal = () => {
  const [path, setPath] = useState("");
  const dispatch = useDispatch();
  const modal = useContext(Modal);

  const onDone = () => {
    dispatch({ type: "workspace/created", payload: path });
    modal.set([]);
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>{"New"} Garden</h3>

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
