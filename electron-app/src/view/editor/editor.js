import { useContext, useRef, useEffect } from "react";
import { useDispatch } from "react-redux";
import {
  addBed,
  setBackground,
  removeBackground,
  workspacePushed,
  undo,
  redo,
} from "../../model/actions";
import { FileInput, NumericTextBox, space, TextBox } from "../common/input";
import { Modal, GardenSVG } from "../../model/context";
import { useState } from "react";
import Nursery from "../nursery";
import Bed from "./bed";
import { downloadText } from "../../storage";
import { RenameGardenModal } from "./rename";
import {
  useBackground,
  useBeds,
  useGarden,
  usePath,
  useRedoAvailable,
  useUndoAvailable,
} from "../../model/selectors";
import { storeData } from "../../model/store";

const Editor = () => {
  const padding = 8;
  const modal = useContext(Modal);

  const outer = useRef(null);
  const inner = useRef(null);

  const [height, setHeight] = useState(0);

  const dispatch = useDispatch();
  const undoAvaliable = useUndoAvailable();
  const redoAvailable = useRedoAvailable();

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

  // TODO: rename `garden` to `beds` in the data structure
  const beds = useBeds();
  const path = usePath();
  const garden = useGarden();

  const handleSave = () => {
    storeData();
  };

  const handleRename = () => {
    modal.put(<RenameGardenModal garden={garden} />);
  };

  const handleLoad = () => {
    dispatch(workspacePushed());
  };

  const handleExport = () => {
    modal.put(<ExportModal garden={garden} />);
  };

  const handleUndo = () => {
    dispatch(undo());
  };

  const handleRedo = () => {
    dispatch(redo());
  };

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
          <h2>{path ? path : "Unnamed Garden"}</h2>
          <button onClick={handleSave} disabled={!path}>
            Save
          </button>
          {space(<button onClick={handleRename}>Rename</button>)}
          {space(<button onClick={handleLoad}>Load</button>)}
          {space(<button onClick={handleExport}>Export</button>)}
          {space(
            <button onClick={handleUndo} disabled={!undoAvaliable}>
              Undo
            </button>
          )}
          {space(
            <button onClick={handleRedo} disabled={!redoAvailable}>
              Redo
            </button>
          )}
          <br />
          <br />
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
          {beds.map((bed) => (
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
  const background = useBackground();
  const dispatch = useDispatch();
  const modal = useContext(Modal);

  const [scale, setScale] = useState(background ? background.scale : 1);
  const [image, setImage] = useState(background ? background.image : null);

  const handleReset = () => {
    setImage(null);
  };

  const onDone = () => {
    dispatch(image ? setBackground(image, scale) : removeBackground());
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Set Background</h3>

      <br />

      {image ? (
        <>
          <img src={image} style={{ width: "60%" }} alt="Preview" />
          <br />
          Scale:{space(<NumericTextBox value={scale} setValue={setScale} />)}
          <button onClick={handleReset}>Reset</button>
        </>
      ) : (
        <FileInput setValue={setImage} />
      )}

      <br />
      <br />
      {space(<button onClick={onDone}>Done</button>)}
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

const ExportModal = ({ garden }) => {
  const modal = useContext(Modal);
  const [exportName, setExportName] = useState(garden.path);
  const gardenSVG = useContext(GardenSVG)[0];

  const handleDownloadImage = () => {
    // TODO: convert to PDF
    // TODO: this implementation captures the current positioning of the camera,
    //       which is undesirable
    downloadText(gardenSVG.outerHTML, exportName + ".html");
  };

  const handleDownloadData = () => {
    downloadText(JSON.stringify(garden), exportName + ".json");
  };

  const onDone = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Export</h3>
      <br />
      Export as: <TextBox value={exportName} setValue={setExportName} />
      <br />
      <br />
      {space(
        <button onClick={handleDownloadImage} disabled={!exportName}>
          Download Image
        </button>
      )}
      {space(
        <button onClick={handleDownloadData} disabled={!exportName}>
          Download Data
        </button>
      )}
      <br />
      <br />
      {space(<button onClick={onDone}>Done</button>)}
    </>
  );
};

export default Editor;
