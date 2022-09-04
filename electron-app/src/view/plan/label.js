const Label = ({ label }) => {
  console.log(label);
  return (
    <text
      x={label.position.x}
      y={label.position.y}
      // Scaling by 10 seems to give reasonable default sizes
      fontSize={label.size / 10}
      style={{ userSelect: "none" }}
    >
      {label.text}
    </text>
  );
};

export default Label;
