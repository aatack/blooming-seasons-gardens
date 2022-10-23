import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { useTemplate } from "../../model/selectors";
import {
  Checkbox,
  ColourPicker,
  Dropdown,
  FileInput,
  NumericTextBox,
  space,
  TextBox,
} from "../common/input";
import { copyElement, editElement, removeElement } from "../../model/actions";
import { Hovered, Modal } from "../../model/context";
import { SVGViewer } from "../common/rendering";

const Plant = ({ plant }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);
  const hovered = useContext(Hovered);

  const template = useTemplate(plant.template);

  const handleMouseEnter = () => {
    hovered.set(plant);
  };

  const handleMouseLeave = () => {
    hovered.set(null);
  };

  const handleEdit = () => {
    modal.put(<EditPlantModal plant={plant} />);
  };

  const handleRemove = () => {
    dispatch(removeElement(plant));
  };

  const handleCopy = () => {
    dispatch(copyElement(plant));
  };

  return (
    <div
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      style={{
        backgroundColor: hovered.matches(plant) ? "lightBlue" : null,
      }}
    >
      <p style={{ display: "inline-block" }}>
        Plant: {template ? template.name : plant.name}
      </p>
      {space(
        <p style={{ display: "inline-block" }}>
          (x = {plant.position.x}, y = {plant.position.y})
        </p>
      )}

      {hovered.matches(plant) &&
        space(<button onClick={handleEdit}>Edit</button>)}
      {hovered.matches(plant) &&
        space(<button onClick={handleRemove}>Remove</button>)}
      {hovered.matches(plant) &&
        space(<button onClick={handleCopy}>Copy</button>)}
    </div>
  );
};

const EditPlantModal = ({ plant }) => {
  const modal = useContext(Modal);
  const dispatch = useDispatch();
  const template = useTemplate(plant.template);

  const [name, setName] = useState(plant.name);
  const [x, setX] = useState(plant.position.x);
  const [y, setY] = useState(plant.position.y);
  const [size, setSize] = useState(plant.size);

  const [iconMode, setIconMode] = useState(plant.iconMode);
  const [iconColour, setIconColour] = useState(plant.iconColour);
  const [iconImage, setIconImage] = useState(plant.iconImage);
  const [iconScale, setIconScale] = useState(plant.iconScale);

  const handleDone = () => {
    if (template) {
      dispatch(editElement(plant, { position: { x: x, y: y } }));
    } else {
      dispatch(
        editElement(plant, {
          position: { x: x, y: y },
          name: name,
          size: size,
          iconMode: iconMode,
          iconColour: iconColour,
          iconImage: iconImage,
          iconScale: iconScale,
        })
      );
    }

    modal.pop();
  };

  const handleCancel = () => {
    modal.pop();
  };

  const handleResetImage = () => {
    setIconImage(null);
  };

  return (
    <>
      <h3>Edit Plant</h3>
      {!template && (
        <>
          <p>Name</p>
          <TextBox value={name} setValue={setName} />
        </>
      )}
      {template && <p>Template: {template.name}</p>}
      <p>Position</p>
      x = <NumericTextBox value={x} setValue={setX} />, y ={" "}
      <NumericTextBox value={y} setValue={setY} />
      {!template && (
        <>
          <p>Size</p>
          <NumericTextBox value={size} setValue={setSize} />
          <p>Icon mode</p>
          <Dropdown
            value={iconMode}
            setValue={setIconMode}
            options={[
              { name: "Colour", key: "colour", value: "colour" },
              { name: "Image", key: "image", value: "image" },
            ]}
          />
          {iconMode === "colour" && (
            <ColourPicker value={iconColour} setValue={setIconColour} />
          )}
          {iconMode === "image" && (
            <>
              <p>Icon</p>
              {iconImage ? (
                <>
                  <SVGViewer isGardenSVG={false}>
                    <image href={iconImage} />
                  </SVGViewer>
                  <br />
                  Scale:
                  {space(
                    <NumericTextBox value={iconScale} setValue={setIconScale} />
                  )}
                  <button onClick={handleResetImage}>Reset</button>
                </>
              ) : (
                <FileInput setValue={setIconImage} />
              )}
            </>
          )}
        </>
      )}
      <br />
      <br />
      <button onClick={handleDone}>Done</button>
      {space(<button onClick={handleCancel}>Cancel</button>)}
    </>
  );
};

export default Plant;
