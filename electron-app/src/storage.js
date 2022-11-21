import { store } from "./model/store";

export const saveData = () => {
  (async () => {
    // TODO: clear the state's history
    const state = store.getState();
    if (!state.garden) {
      console.error("Potentially saving empty data");
    }

    const rawResponse = await fetch("/save", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(state),
    });

    const status = await rawResponse.json();
    if (status !== 200) {
      console.error("Error saving to disk");
    }
  })();
};

export const encodeFile = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
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
