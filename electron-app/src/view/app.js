import { useDispatch, useSelector } from "react-redux";

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

  const handleClick = () => {
    dispatch({ type: "garden/bed/removed", payload: bed.identifier });
  };

  return (
    <>
      <p>{bed.name}</p>
      <button onClick={handleClick}>Remove</button>
    </>
  );
};

export default App;
