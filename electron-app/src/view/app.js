import { useDispatch, useSelector } from "react-redux";

const App = () => {
  return (
    <>
      <p>Testing redux with react and electron</p>
      <Counter />
      <Increment />
      <Decrement />
    </>
  );
};

const Counter = () => {
  const value = useSelector((state) => state.value);
  return <p>{value}</p>;
};

const Increment = () => {
  const dispatch = useDispatch();

  const handleClick = () => {
    dispatch({ type: "incremented" });
  };

  return <button onClick={handleClick}>Increment</button>;
};

const Decrement = () => {
  const dispatch = useDispatch();

  const handleClick = () => {
    dispatch({ type: "decremented" });
  };

  return <button onClick={handleClick}>Decrement</button>;
};

export default App;
