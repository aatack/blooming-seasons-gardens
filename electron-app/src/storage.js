const activeGardenPrefix = "blooming-seasons/active/";
const deletedGardenPrefix = "blooming-seasons/deleted/";

export const encodeFile = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
};

export const saveGarden = (garden) => {
  localStorage.setItem(
    activeGardenPrefix + garden.path,
    JSON.stringify(garden)
  );
};

export const loadGarden = (path) => {
  return JSON.parse(localStorage.getItem(activeGardenPrefix + path));
};

export const deleteGarden = (path) => {
  // NOTE: although gardens can be recovered, their original names will not
  //       necessarily be available any more.  Recover manually for now, but in
  //       future force a rename when recovering
  localStorage.setItem(deletedGardenPrefix + path, loadGarden(path));
  localStorage.removeItem(activeGardenPrefix + path);
};

export const listGardens = () => {
  const gardens = [];
  for (var i = 0, length = localStorage.length; i < length; ++i) {
    const key = localStorage.key(i);
    if (key.includes(activeGardenPrefix)) {
      gardens.push(localStorage.key(i).replace(activeGardenPrefix, ""));
    }
  }
  return gardens;
};

export const listDeletedGardens = () => {
  const gardens = [];
  for (var i = 0, length = localStorage.length; i < length; ++i) {
    const key = localStorage.key(i);
    if (key.includes(deletedGardenPrefix)) {
      gardens.push(localStorage.key(i).replace(deletedGardenPrefix, ""));
    }
  }
  return gardens;
};
