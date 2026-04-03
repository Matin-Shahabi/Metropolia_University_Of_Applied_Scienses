"use strict";
let rolls = Number(prompt("How many dice rolls?"));
let sum = 0;

for (let i = 0; i < rolls; i++) {
  let dice = Math.floor(Math.random() * 6) + 1;
  sum += dice;
}

console.log("Sum:", sum);
document.body.innerHTML = `Sum : ${sum}`;
