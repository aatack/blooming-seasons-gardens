import React, { useState } from "react";

const ModalContext = React.createContext(undefined);
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

export const Modal = {
  Context: ModalContext,
  Provider: ({ children }) => {
    return (
      <ModalContext.Provider value={useModal()}>
        {children}
      </ModalContext.Provider>
    );
  },
};
