import React, { useState, useContext } from "react";

export const Modal = (() => {
  const Context = React.createContext(undefined);

  const CachedProvider = Context.Provider;

  const useModal = () => {
    const [modal, privateSetModal] = useState(null);

    const publicSetModal = (newModal) => {
      console.log(typeof newModal, newModal);
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
        <div onClick={closeModal} className="modal-background">
          <div
            onClick={(e) => e.stopPropagation()}
            className="modal-foreground"
          >
            {modal.modal}
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
