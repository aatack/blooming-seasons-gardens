import React, { useState, useContext } from "react";

export const Modal = (() => {
  const Context = React.createContext(undefined);

  const CachedProvider = Context.Provider;

  const useModal = () => {
    const [modals, setModals] = useState([]);

    return {
      get: () => (modals.length > 0 ? modals[0] : null),
      put: (modal) => {
        setModals(modal ? [modal].concat(modals) : modals);
      },
      pop: () => {
        setModals(modals.slice(1));
      },
      set: (stack) => {
        setModals(stack);
      },
    };
  };

  const WrappedProvider = (props) => {
    return <CachedProvider value={useModal()}>{props.children}</CachedProvider>;
  };

  const WrappedComponent = () => {
    const manager = useContext(Context);

    const closeModal = () => {
      manager.set([]);
    };

    const modal = manager.get();
    if (modal) {
      return (
        <div onClick={closeModal} className="modal-background">
          <div
            onClick={(e) => e.stopPropagation()}
            className="modal-foreground"
          >
            {modal}
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

export const GardenSVG = React.createContext(undefined);

export const Hovered = (() => {
  const Context = React.createContext(undefined);

  const CachedProvider = Context.Provider;

  const useHovered = () => {
    const [hovered, setHovered] = useState(null);

    return {
      matches: (element) => hovered === element.identifier,
      set: (element) => {
        setHovered(element.identifier);
      },
    };
  };

  const WrappedProvider = (props) => {
    return (
      <CachedProvider value={useHovered()}>{props.children}</CachedProvider>
    );
  };

  Context.Provider = WrappedProvider;
  return Context;
})();
