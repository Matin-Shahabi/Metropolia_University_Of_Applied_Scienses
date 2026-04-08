"use strict";
let numbers = [];

while (true) {
  let num = Number(prompt("Enter a number (0 to stop):"));

  if (num === 0) break;

  numbers.push(num);
}

numbers.sort((a, b) => b - a);

for (let i = 0; i < numbers.length; i++) {
  console.log(numbers[i]);
}