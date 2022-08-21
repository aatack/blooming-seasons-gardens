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
