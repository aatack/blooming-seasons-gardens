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
      matches: (element, includeParents) =>
        hovered === element.identifier ||
        (includeParents && hovered === element.bedIdentifier),
      set: (element) => {
        if (element) {
          setHovered(element.identifier);
        } else {
          setHovered(null);
        }
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

export const Selected = (() => {
  const Context = React.createContext(undefined);

  const CachedProvider = Context.Provider;

  const useSelected = () => {
    const [selected, setSelected] = useState(null);

    return {
      matches: (element, includeParents) =>
        selected === element.identifier ||
        (includeParents && selected === element.bedIdentifier),
      set: (element) => {
        if (element) {
          setSelected(element.identifier);
        } else {
          setSelected(null);
        }
      },
      get: () => selected,
    };
  };

  const WrappedProvider = (props) => {
    return (
      <CachedProvider value={useSelected()}>{props.children}</CachedProvider>
    );
  };

  Context.Provider = WrappedProvider;
  return Context;
})();

export const PlanX = React.createContext(undefined);
export const PlanY = React.createContext(undefined);
export const PlanScale = React.createContext(undefined);
