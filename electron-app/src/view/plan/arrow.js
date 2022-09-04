const Arrow = ({ arrow }) => {
  return (
    <line
      x1={arrow.start.x}
      x2={arrow.end.x}
      y1={arrow.start.y}
      y2={arrow.end.y}
      stroke="black"
      // Scaling by 50 seems to give a reasonable default width
      strokeWidth={arrow.width / 50}
    />
  );
};

export default Arrow;
