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
  if (garden.path) {
    localStorage.setItem(
      activeGardenPrefix + garden.path,
      JSON.stringify(garden)
    );
  }
};

export const loadGarden = (path) => {
  return JSON.parse(localStorage.getItem(activeGardenPrefix + path));
};

export const deleteGarden = (path) => {
  // TODO: at some point, deleted gardens will need to be garbage collected

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

export const downloadText = (text, fileName) => {
  const link = document.createElement("a");

  link.setAttribute(
    "href",
    "data:text/plain;charset=utf-8," + encodeURIComponent(text)
  );
  link.setAttribute("download", fileName);

  link.style.display = "none";
  document.body.appendChild(link);

  link.click();

  document.body.removeChild(link);
};
