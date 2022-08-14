import { useContext } from "react";
import { Modal } from "../model/context";

export const Popup = () => {
  const [modal, _] = useContext(Modal);

  if (modal) {
    return <div>{modal.element}</div>;
  } else {
    return null;
  }
};
