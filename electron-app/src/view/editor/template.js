import { useDispatch } from "react-redux";
import { useContext, useState } from "react";
import { removeTemplate } from "../../model/actions";
import { Modal } from "../../model/context";
import { PlantSVG } from "../plan/plant";
import { EditPlantModal } from "./plant";
import { EditLabelModal } from "./label";
import { space } from "../common/input";

const Template = ({ template }) => {
  const dispatch = useDispatch();

  const modal = useContext(Modal);
  const [hovered, setHovered] = useState(false);

  const handleRemoveTemplate = () => {
    dispatch(removeTemplate(template));
  };

  const handleEdit = () => {
    switch (template.type) {
      case "plant":
        modal.put(<EditPlantModal plant={template} />);
        break;
      case "label":
        modal.put(<EditLabelModal label={template} />);
        break;
      default:
        console.error(`Unknown template type: ${template.type}`);
    }
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
      {template.type === "plant" && (
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
      )}
      {space(
        <p style={{ display: "inline-block" }}>
          {template.name || template.text}
        </p>
      )}

      {hovered && space(<button onClick={handleRemoveTemplate}>Remove</button>)}
      {hovered && space(<button onClick={handleEdit}>Edit</button>)}
    </div>
  );
};

export default Template;
