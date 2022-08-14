import { useDispatch, useSelector } from "react-redux";
import { addBed } from "../../model/store";
import Bed from "./bed";

const Editor = () => {
  const dispatch = useDispatch();

  const handleAddBed = () => {
    dispatch(addBed());
  };

  const garden = useSelector((state) => state.garden);
  return (
    <div style={{ backgroundColor: "lightGrey", padding: 8 }}>
      <button onClick={handleAddBed}>Add Bed</button>
      {garden.map((bed) => (
        <Bed bed={bed} key={bed.identifier} />
      ))}
    </div>
  );
};

export default Editor;
