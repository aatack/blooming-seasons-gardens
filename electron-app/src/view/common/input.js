import { useState } from "react";

// TODO: look into React's handling of forms
// TODO: have all of the widgets take the output of `useState` directly
// TODO: add labels to each of these

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

export const NumericTextBox = (props) => {
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

export const ColourPicker = (props) => {
  const [value, setValue] = useState(props.value);

  const handleChange = (e) => {
    setValue(e.target.value);
    if (props.setValue) {
      props.setValue(e.target.value);
    }
  };

  return <input type="color" value={value} onChange={handleChange}></input>;
};

export const Checkbox = (props) => {
  const [value, setValue] = useState(props.value);

  const handleChange = (e) => {
    setValue(e.target.checked);
    if (props.setValue) {
      props.setValue(e.target.checked);
    }
  };

  return <input type="checkbox" value={value} onChange={handleChange} />;
};

export const Dropdown = (props) => {
  // Expects `options` to be an array of objects with `name` and `identifier`
  // keys

  const [value, setValue] = useState(props.value.name);

  const handleChange = (e) => {
    const newValue = props.options.find(
      (option) => option.name == e.target.value
    );
    setValue(newValue.name);

    if (props.setValue) {
      props.setValue(newValue);
    }
  };

  return (
    <select onChange={handleChange} value={value}>
      {props.options.map((option) => (
        <option key={option.identifier.toString()}>{option.name}</option>
      ))}
    </select>
  );
};

export const space = (element) => {
  return (
    <>
      &nbsp;
      {element}
    </>
  );
};
