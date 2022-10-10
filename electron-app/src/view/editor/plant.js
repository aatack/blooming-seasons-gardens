import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { useTemplate } from "../../model/selectors";
import {
  Checkbox,
  ColourPicker,
  FileInput,
  NumericTextBox,
  space,
  TextBox,
} from "../common/input";
import { copyElement, editElement, removeElement } from "../../model/actions";
import { Hovered, Modal } from "../../model/context";

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

  const [useColour, setUseColour] = useState(plant.setUseColour);
  const [colour, setColour] = useState(plant.colour);
  const [icon, setIcon] = useState(plant.icon);

  const handleDone = () => {
    if (template) {
      dispatch(editElement(plant, { position: { x: x, y: y } }));
    } else {
      dispatch(
        editElement(plant, {
          position: { x: x, y: y },
          name: name,
          size: size,
          colour: colour,
          icon: icon,
        })
      );
    }

    modal.pop();
  };

  const handleCancel = () => {
    modal.pop();
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
          <IconPicker
            colour={colour}
            setColour={setColour}
            icon={icon}
            setIcon={setIcon}
            useColour={useColour}
            setUseColour={setUseColour}
          />
        </>
      )}
      <br />
      <br />
      <button onClick={handleDone}>Done</button>
      {space(<button onClick={handleCancel}>Cancel</button>)}
    </>
  );
};

const IconPicker = ({
  colour,
  setColour,
  icon,
  setIcon,
  useColour,
  setUseColour,
}) => {
  const [scale, setScale] = useState(icon.scale);
  const [image, setImage] = useState(icon.image);

  // TODO: surely there's a neater way than this...?

  const wrappedSetScale = (newScale) => {
    setScale(newScale);
    setIcon({ ...icon, scale: newScale });
  };

  const wrappedSetImage = (newImage) => {
    setImage(newImage);
    setIcon({ ...icon, image: newImage });
  };

  const handleReset = () => {
    setImage(null);
  };

  return (
    <>
      <p>Use colour?</p>
      <Checkbox value={useColour} setValue={setUseColour} />
      {useColour && (
        <>
          <p>Colour</p>
          <ColourPicker value={colour} setValue={setColour} />
        </>
      )}
      {!useColour && (
        <>
          <p>Icon</p>
          {image ? (
            <>
              <img src={image} style={{ width: "60%" }} alt="Preview" />
              <br />
              Scale:
              {space(
                <NumericTextBox value={scale} setValue={wrappedSetScale} />
              )}
              <button onClick={handleReset}>Reset</button>
            </>
          ) : (
            <FileInput setValue={wrappedSetImage} />
          )}
        </>
      )}
    </>
  );
};

export default Plant;
