const express = require("express");
const fs = require("fs");

const PORT = 3001;

const defaultState = {
  garden: null,
  history: {
    index: 0,
    items: [],
  },
  workspace: {
    identifier: 1,
    gardens: [],
  },
};

const app = express();

app.use(express.json({ limit: "1gb" }));

app.get("/load", (request, response) => {
  var message;
  if (fs.existsSync("data/store.json")) {
    message = JSON.parse(fs.readFileSync("data/store.json").toString());
  } else {
    message = defaultState;
  }
  response.json({ message: message });
});

app.post("/save", (request, response) => {
  fs.writeFileSync("data/store.json", JSON.stringify(request.body));
  response.send(200);
});

app.listen(PORT, () => {
  console.log(`Server listening on ${PORT}`);
});
