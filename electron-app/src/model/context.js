import React, { useState } from "react";

export const Modal = (() => {
  const Modal = React.createContext(undefined);

  const CachedModalProvider = Modal.Provider;

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

  const WrappedModalProvider = (props) => {
    return (
      <CachedModalProvider value={useModal()}>
        {props.children}
      </CachedModalProvider>
    );
  };

  Modal.Provider = WrappedModalProvider;
  return Modal;
})();
