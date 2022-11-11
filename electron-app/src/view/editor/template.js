import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import { editTemplate, removeTemplate } from "../../model/actions";
import { Modal } from "../../model/context";
import { ColourPicker, NumericTextBox, space, TextBox } from "../common/input";
import { Dropdown, FileInput } from "../common/input";
import { SVGViewer, StaticSVG } from "../common/rendering";

const Template = ({ template }) => {
  const dispatch = useDispatch();

  const modal = useContext(Modal);
  const [hovered, setHovered] = useState(false);

  const handleRemoveTemplate = () => {
    dispatch(removeTemplate(template));
  };

  const handleEdit = () => {
    modal.put(<EditTemplateModal template={template} />);
  };

  const handleMouseEnter = () => {
    setHovered(true);
  };

  const handleMouseLeave = () => {
    setHovered(false);
  };

  return (
    <div onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
      <p style={{ display: "inline-block" }}>{template.name}</p>

      {hovered && space(<button onClick={handleRemoveTemplate}>Remove</button>)}
      {hovered && space(<button onClick={handleEdit}>Edit</button>)}
    </div>
  );
};

const OldEditTemplateModal = ({ template }) => {
  const dispatch = useDispatch();
  const modal = useContext(Modal);

  const [name, setName] = useState(template.name);
  const [size, setSize] = useState(template.size);
  const [colour, setColour] = useState(template.colour);

  const onDone = () => {
    dispatch(editTemplate(template.identifier, name, size, colour));
    modal.pop();
  };

  const onCancel = () => {
    modal.pop();
  };

  return (
    <>
      <h3>Edit Template</h3>

      <p>Name</p>
      <TextBox value={name} setValue={setName} />

      <p>Size</p>
      <NumericTextBox value={size} setValue={setSize} />

      <p>Colour</p>
      <ColourPicker value={colour} setValue={setColour} />

      <br />
      <br />

      <button onClick={onDone}>Done</button>
      {space(<button onClick={onCancel}>Cancel</button>)}
    </>
  );
};

const EditTemplateModal = ({ template }) => {
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const [name, setName] = useState(template.name);
  const [size, setSize] = useState(template.size);

  const [iconMode, setIconMode] = useState(template.iconMode);
  const [iconColour, setIconColour] = useState(template.iconColour);
  const [iconImage, setIconImage] = useState(template.iconImage);
  const [iconX, setIconX] = useState(template.iconX);
  const [iconY, setIconY] = useState(template.iconY);
  const [iconScale, setIconScale] = useState(template.iconScale);

  const handleDone = () => {
    dispatch(
      editTemplate(template.identifier, {
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

  return (
    <>
      <h3>Edit Template</h3>
      {!template && (
        <>
          <p>Name</p>
          <TextBox value={name} setValue={setName} />
        </>
      )}
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
              <SVGViewer
                isGardenSVG={false}
                scrollSensitivity={0.0008}
                bindX={[iconX, setIconX]}
                bindY={[iconY, setIconY]}
                bindScale={[iconScale, setIconScale]}
              >
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
      <br />
      <br />
      <button onClick={handleDone}>Done</button>
      {space(<button onClick={handleCancel}>Cancel</button>)}
    </>
  );
};

export default Template;
