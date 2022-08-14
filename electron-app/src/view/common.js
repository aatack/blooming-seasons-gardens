import { useContext } from "react";
import { Modal } from "../model/context";

export const Popup = () => {
  const [modal, setModal] = useContext(Modal);

  const closeModal = () => {
    setModal(null);
  };

  if (modal) {
    return (
      <div
        onClick={closeModal}
        style={{
          position: "fixed",
          zIndex: 1,
          left: 0,
          top: 0,
          width: "100%",
          height: "100%",
          overflow: "auto",
          backgroundColor: "rgba(0, 0, 0, 0.4)",
        }}
      >
        <div
          onClick={(e) => {
            e.stopPropagation();
          }}
          style={{
            backgroundColor: "#fefefe",
            margin: "15% auto",
            padding: "20px",
            border: "1px solid #888",
            width: "80%",
          }}
        >
          {modal.element}
        </div>
      </div>
    );
  } else {
    return null;
  }
};
