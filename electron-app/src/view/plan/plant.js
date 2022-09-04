import { useTemplate } from "../../model/selectors";

const Plant = ({ plant }) => {
  const template = useTemplate(plant.template);

  if (template) {
    plant = { ...template, ...plant };
  }

  return (
    <circle
      cx={plant.position.x}
      cy={plant.position.y}
      r={plant.size}
      fill={plant.colour}
      stroke="black"
      strokeWidth={plant.size / 5}
    />
  );
};

export default Plant;
