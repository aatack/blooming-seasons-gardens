import { useDispatch, useSelector } from "react-redux";
import { useState } from "react";

const App = () => {
  return (
    <>
      <AddBed />
      <Garden />
    </>
  );
};

const AddBed = () => {
  const dispatch = useDispatch();

  const handleClick = () => {
    dispatch({ type: "garden/bed/added" });
  };

  return <button onClick={handleClick}>Add Bed</button>;
};

const Garden = () => {
  const garden = useSelector((state) => state.garden);
  return garden.map((bed) => <Bed bed={bed} key={bed.identifier} />);
};

const Bed = ({ bed }) => {
  const dispatch = useDispatch();

  const [hovered, setHovered] = useState(false);

  const handleRemoveClick = () => {
    dispatch({ type: "garden/bed/removed", payload: bed.identifier });
  };

  const handleRenameClick = () => {
    dispatch({
      type: "garden/bed/renamed",
      payload: {
        identifier: bed.identifier,
        name: bed.name + "?",
      },
    });
  };

  const handleMouseEnter = () => {
    setHovered(true);
  };

  const handleMouseLeave = () => {
    setHovered(false);
  };

  return (
    <div onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
      <p style={{ display: "inline-block" }}>{bed.name}</p>
      <button
        style={{ display: hovered ? "inline-block" : "none" }}
        onClick={handleRemoveClick}
      >
        Remove
      </button>
      <button
        style={{ display: hovered ? "inline-block" : "none" }}
        onClick={handleRenameClick}
      >
        Rename
      </button>
    </div>
  );
};

export default App;
