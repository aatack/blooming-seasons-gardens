import { useState } from "react";

export const TextBox = (props) => {
  const [value, setValue] = useState(props.value);

  const handleChange = (e) => {
    setValue(e.target.value);
    if (props.setValue) {
      props.setValue(e.target.value);
    }
  };

  return <input value={value} onChange={handleChange}></input>;
};

export const NumberBox = (props) => {
  // TODO: look into React's handling of forms

  const [value, setValue] = useState(props.value.toString());
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setValue(e.target.value);

    const numericValue = parseFloat(e.target.value);
    if (!isNaN(numericValue)) {
      if (props.setValue) {
        props.setValue(numericValue);
      }
      setError(null);
    } else {
      setError("Error: size must be a number");
    }
  };
  return (
    <>
      {error && <p>{error}</p>}
      <input value={value} onChange={handleChange}></input>
    </>
  );
};
