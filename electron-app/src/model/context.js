import React, { useState, useContext } from "react";

export const Modal = (() => {
  const Context = React.createContext(undefined);

  const CachedProvider = Context.Provider;

  const useModal = () => {
    const [modal, privateSetModal] = useState(null);

    const publicSetModal = (newModal) => {
      if (modal && modal.onClose) {
        modal.onClose();
      }
      privateSetModal(newModal);
    };

    return [modal, publicSetModal];
  };

  const WrappedProvider = (props) => {
    return <CachedProvider value={useModal()}>{props.children}</CachedProvider>;
  };

  const WrappedComponent = () => {
    const [modal, setModal] = useContext(Context);

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

  Context.Provider = WrappedProvider;
  Context.Component = WrappedComponent;
  return Context;
})();
