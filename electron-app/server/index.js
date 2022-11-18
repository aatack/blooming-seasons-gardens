const express = require("express");
const fs = require("fs");

const PORT = 3001;

const app = express();

app.get("/api", (req, res) => {
  res.json({
    message: JSON.parse(fs.readFileSync("data/test.json").toString()),
  });
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
