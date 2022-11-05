import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { useTemplate } from "../../model/selectors";
import {
  ColourPicker,
  Dropdown,
  FileInput,
  NumericTextBox,
  space,
  TextBox,
} from "../common/input";
import { copyElement, editElement, removeElement } from "../../model/actions";
import { Hovered, Modal } from "../../model/context";
import { StaticSVG, SVGViewer } from "../common/rendering";

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
  const [iconX, setIconX] = useState(plant.iconX);
  const [iconY, setIconY] = useState(plant.iconY);

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
          iconX: iconX,
          iconY: iconY,
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

  const handleResetPositioning = () => {
    setIconScale(1);
    setIconX(0);
    setIconY(0);
  };

  const bindX = useState(0)
  const bindY = useState(0)
  const bindScale = useState(1)

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
              <p>
                Drag the image to position it inside the circle. Use the scroll
                wheel to resize it.
              </p>
              {iconImage ? (
                <div
                  style={{
                    height: "240px",
                    width: "240px",
                    marginBottom: "10px",
                  }}
                >
                  <SVGViewer isGardenSVG={false} scrollSensitivity={0.0008}
                    bindX={bindX} bindY={bindY} bindScale={bindScale}>
                    <>
                      <image href={iconImage} />
                      <StaticSVG>
                        <circle
                          cx={120}
                          cy={120}
                          r={100}
                          fill="none"
                          stroke="grey"
                          strokeWidth={1}
                        />
                      </StaticSVG>
                    </>
                  </SVGViewer>
                  <br />
                  <button onClick={handleResetImage}>Reset image</button>
                  {space(
                    <button onClick={handleResetPositioning}>
                      Reset positioning
                    </button>
                  )}
                  <br />
                  <br />
                </div>
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
