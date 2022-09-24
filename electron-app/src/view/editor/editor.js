import { useContext, useRef, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addBed, changeBackground } from "../../model/store";
import { FileInput, space, TextBox } from "../common/input";
import { Modal } from "../../model/context";
import { useState } from "react";
import Nursery from "./nursery";
import Bed from "./bed";

const Editor = () => {
  const padding = 8;
  const modal = useContext(Modal);

  const outer = useRef(null);
  const inner = useRef(null);

  const [height, setHeight] = useState(0);

  const handleAddBed = () => {
    modal.put(<CreateBedModal />);
  };

  const handleViewNursery = () => {
    modal.put(<Nursery />);
  };

  const handleSetBackground = () => {
    modal.put(<SetBackgroundModal />);
  };

  useEffect(() => {
    setHeight(outer.current.clientHeight - inner.current.clientHeight);
  }, []);

  const garden = useSelector((state) => state.garden);
  return (
    <div
      ref={outer}
      style={{
        backgroundColor: "lightGrey",
        width: "100%",
        height: "100%",
      }}
    >
      <div
        style={{
          padding: padding,
          display: "table",
          width: "100%",
          height: "100%",
          boxSizing: "border-box",
        }}
      >
        <div ref={inner}>
          <button onClick={handleAddBed}>Add Bed</button>
          {space(<button onClick={handleViewNursery}>View Nursery</button>)}
          {space(<button onClick={handleSetBackground}>Set Background</button>)}
        </div>

        <div
          style={{
            height: height - padding * 2,
            overflowY: "auto",
            overflowX: "hidden",
            boxSizing: "border-box",
            paddingTop: "calc(vw - 100%)",
          }}
        >
          {garden.map((bed) => (
            <Bed bed={bed} key={bed.identifier} />
          ))}
        </div>
      </div>
    </div>
  );
};

const CreateBedModal = () => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const [name, setName] = useState("");

  const onDone = () => {
    dispatch(addBed(name));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Create Bed</h3>
      <TextBox value={name} setValue={setName} />
      {space(<button onClick={onDone}>Done</button>)}
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

const SetBackgroundModal = () => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const [background, setBackground] = useState(null);

  const onDone = async () => {
    dispatch(await changeBackground(background));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Set Background</h3>
      <FileInput setValue={setBackground} />
      <br />
      <br />
      {space(
        <button onClick={onDone}>{background ? "Done" : "Remove"}</button>
      )}
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

export default Editor;
