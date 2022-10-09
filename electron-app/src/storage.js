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
