import React, { useState } from "react";

export const Modal = React.createContext(undefined);

export const useModal = () => {
  const [modal, privateSetModal] = useState(null);

  const publicSetModal = (newModal) => {
    if (modal && modal.onClose) {
      modal.onClose();
    }
    privateSetModal(newModal);
  };

  return [modal, publicSetModal];
};
