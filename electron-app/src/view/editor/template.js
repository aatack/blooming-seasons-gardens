import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import { editTemplate, removeTemplate } from "../../model/actions";
import { Modal } from "../../model/context";
import { ColourPicker, NumericTextBox, space, TextBox } from "../common/input";
import { Dropdown, FileInput } from "../common/input";
import { SVGViewer, StaticSVG } from "../common/rendering";
import { PlantSVG } from "../plan/plant";

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

  const previewSize = 30;

  return (
    <div onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
      <svg style={{ width: `${previewSize}px`, height: `${previewSize}px` }}>
        <PlantSVG
          plant={{
            ...template,
            position: { x: previewSize / 2, y: previewSize / 2 },
            size: previewSize,
            border: (template.border / template.size) * previewSize,
          }}
        />
      </svg>
      {space(<p style={{ display: "inline-block" }}>{template.name}</p>)}

      {hovered && space(<button onClick={handleRemoveTemplate}>Remove</button>)}
      {hovered && space(<button onClick={handleEdit}>Edit</button>)}
    </div>
  );
};

const EditTemplateModal = ({ template }) => {
  const modal = useContext(Modal);
  const dispatch = useDispatch();

  const [name, setName] = useState(template.name);
  const [size, setSize] = useState(template.size);
  const [border, setBorder] = useState(template.border);

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
        border: border,
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
      <p>Border</p>
      <NumericTextBox value={border} setValue={setBorder} />
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
