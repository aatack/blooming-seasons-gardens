const express = require("express");
const fs = require("fs");

const PORT = 3001;

const app = express();

app.get("/load-data", (req, res) => {
  res.json({
    message: JSON.parse(fs.readFileSync("data/saved-data.json").toString()),
  });
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
