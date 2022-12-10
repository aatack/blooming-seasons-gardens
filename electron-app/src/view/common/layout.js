import { clamp } from "./maths";
import { useContext, useState } from "react";
import { useDispatch } from "react-redux";
import { editElement, redo, undo } from "../../model/actions";
import { useElement } from "../../model/selectors";
import { Selected } from "../../model/context";
import { PlanX, PlanY, PlanScale } from "../../model/context";

export const HorizontalSplit = ({
  children,
  dragWidth,
  minimumWidth,
  initialWidth,
  toggleKey,
}) => {
  const [first, second] = children.props.children;

  const [width, setWidth] = useState(initialWidth);
  const [x, setX] = useState(null);
  const [collapsed, setCollapsed] = useState(false);

  const selectedElement = useElement(useContext(Selected).get());

  const [_x, setPlanX] = useContext(PlanX);
  const [_y, setPlanY] = useContext(PlanY);
  const [_scale, setPlanScale] = useContext(PlanScale);

  const dispatch = useDispatch();

  const handleDragStart = (e) => {
    setX(e.clientX);
  };

  const handleDrag = (e) => {
    if (e.clientX) {
      // TODO: stop the mouse from moving away from the drag box at the extremes
      setWidth(
        clamp(
          width - x + e.clientX,
          minimumWidth,
          window.innerWidth - minimumWidth
        )
      );
      setX(e.clientX);
    }
  };

  const handleClick = () => {
    setCollapsed(!collapsed);
  };

  const handleKeyDown = (e) => {
    if (e.which === toggleKey) {
      setCollapsed(!collapsed);
    }

    if (e.code === "KeyZ" && e.ctrlKey) {
      dispatch(undo());
    }

    if (e.code === "KeyY" && e.ctrlKey) {
      dispatch(redo());
    }

    if (e.code === "KeyH") {
      setPlanX(0);
      setPlanY(0);
      setPlanScale(100);
    }

    if (selectedElement) {
      var dx = 0;
      var dy = 0;

      if (e.code === "ArrowLeft") {
        dx = -1;
      }
      if (e.code === "ArrowRight") {
        dx = 1;
      }
      if (e.code === "ArrowUp") {
        dy = -1;
      }
      if (e.code === "ArrowDown") {
        dy = 1;
      }

      if (selectedElement.position && (dx !== 0 || dy !== 0)) {
        const position = selectedElement.position;
        const step = e.ctrlKey ? 0.5 : e.shiftKey ? 0.02 : 0.1;

        dispatch(
          editElement(selectedElement, {
            position: { x: position.x + dx * step, y: position.y + dy * step },
          })
        );
      }
    }
  };

  return (
    <div onKeyDown={handleKeyDown} tabIndex={0}>
      {!collapsed && (
        <div
          style={{
            position: "fixed",
            height: "100%",
            left: "0%",
            width: width,
            top: "0%",
          }}
        >
          {first}
        </div>
      )}
      <div
        style={{
          position: "fixed",
          height: "100%",
          left: collapsed ? 0 : width,
          right: "0%",
          top: 0,
        }}
      >
        {second}
      </div>
      <div
        style={{
          position: "fixed",
          height: "100%",
          left: collapsed ? 0 : width - dragWidth,
          width: collapsed ? dragWidth * 2 : dragWidth,
          top: 0,
          cursor: "ew-resize",
        }}
        draggable={true}
        onDragStart={handleDragStart}
        onDrag={handleDrag}
        onClick={handleClick}
      />
    </div>
  );
};
