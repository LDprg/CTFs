const forgeHash = (data, payload) =>
  JSON.stringify([payload, { length: -payload.length }, [...data]]);

const sha = require("sha.js");
const { randomBytes } = require("crypto");

const sha256 = (...messages) => {
  const hash = sha("sha256");
  messages.forEach((m) => hash.update(m));
  return hash.digest("hex");
};

const validMessage = [randomBytes(32), randomBytes(32), randomBytes(32)]; // whatever

const payload = forgeHash(
  Buffer.concat(validMessage),
  "Hashed input means safe",
);
const receivedMessage = JSON.parse(payload); // e.g. over network, whatever

console.log(sha256(...validMessage));
console.log(sha256(...receivedMessage));
console.log(receivedMessage[0]);
console.log();

let buf = ["a", randomBytes(9).toString("hex")];
let buf_broke = { length: buf.length, ...buf, 0: buf[0] + 256, 1: "test" };

console.log(sha256(buf_broke));
console.log(sha256(buf));
console.log(buf_broke[1]);
console.log(buf[1]);

console.log();

const header = { alg: "HS256", typ: "JWT" };
const secret2 = randomBytes(9).toString("hex");
const payload2 = {
  username: "admin",
  exp: Math.floor(Date.now() / 1000) + 3600,
  length: secret2.length,
};
const signature = sha256(...[JSON.stringify(header), payload2, secret2]);

const secret = randomBytes(9).toString("hex");
const expectedSignatureHex = sha256(
  ...[JSON.stringify(header), payload2, secret],
);

console.log(expectedSignatureHex);
console.log(signature);
