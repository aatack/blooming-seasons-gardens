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
  return garden.map((bed) => <p key={bed.identifier}>{bed.name}</p>);
};

export default App;
