export const saveGarden = (identifier, garden) => {
  console.log(garden);
  console.log(JSON.stringify(garden));
  localStorage.setItem(
    "blooming-seasons/" + identifier,
    JSON.stringify(garden)
  );
};

export const loadGarden = (identifier) => {
  return JSON.parse(localStorage.getItem("blooming-seasons/" + identifier));
};

export const encodeFile = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};
