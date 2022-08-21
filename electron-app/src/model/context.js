import React, { useState, useContext } from "react";

export const Modal = (() => {
  const Context = React.createContext(undefined);

  const CachedProvider = Context.Provider;

  const useModal = () => {
    const [modals, setModals] = useState([]);

    return {
      get: () => (modals.length > 0 ? modals[modals.length - 1] : null),
      set: (modal) => {
        for (const openModal in modals) {
          if (openModal.onClose) {
            openModal.onClose();
          }
        }
        setModals(modal ? [modal] : []);
      },
    };

    // const publicSetModal = (newModal) => {
    //   if (modal && modal.onClose) {
    //     modal.onClose();
    //   }
    //   privateSetModal(newModal);
    // };

    // return [modal, publicSetModal];
  };

  const WrappedProvider = (props) => {
    return <CachedProvider value={useModal()}>{props.children}</CachedProvider>;
  };

  const WrappedComponent = () => {
    const manager = useContext(Context);

    const closeModal = () => {
      manager.set();
    };

    const modal = manager.get();
    if (modal) {
      if (!modal.modal) {
        console.warn(
          "Modal needs to be wrapped in an object with a `modal` key",
          modal
        );
      }

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
