export const saveGarden = (garden) => {
  localStorage.setItem(
    "blooming-seasons/" + garden.path,
    JSON.stringify(garden)
  );
};

export const loadGarden = (path) => {
  return JSON.parse(localStorage.getItem("blooming-seasons/" + path));
};

export const encodeFile = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};
