"use strict";
let numbers = [];

while (true) {
  let num = Number(prompt("Enter a number:"));

  if (numbers.includes(num)) {
    alert("Number already given!");
    break;
  }

  numbers.push(num);
}

numbers.sort((a, b) => a - b);

for (let i = 0; i < numbers.length; i++) {
  console.log(numbers[i]);
}