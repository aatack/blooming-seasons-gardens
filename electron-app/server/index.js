const express = require("express");
const fs = require("fs");

const PORT = 3001;

const app = express();

app.use(express.json());

app.get("/load", (request, response) => {
  response.json({
    message: JSON.parse(fs.readFileSync("data/store.json").toString()),
  });
});

app.post("/save", (request, response) => {
  fs.writeFileSync("data/store.json", JSON.stringify(request.body));
  response.send(200);
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
