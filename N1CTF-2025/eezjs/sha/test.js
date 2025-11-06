const test = () => {
  return null;
};

var abc = {};
// abc.__proto__.a = true;
abc.__proto__ = true;

var a = {};

console.log(a.a);

if (test()) {
  console.log("workes");
}
