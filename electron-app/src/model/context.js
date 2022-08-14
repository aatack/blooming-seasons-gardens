import React, { useState } from "react";

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

  Context.Provider = WrappedProvider;
  return Context;
})();
