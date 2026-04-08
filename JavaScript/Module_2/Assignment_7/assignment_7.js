"use strict";
function rollDice(sides) {
  return Math.floor(Math.random() * sides) + 1;
}

let sides = Number(prompt("Enter number of sides:"));
let rolls = [];
let result;

do {
  result = rollDice(sides);
  rolls.push(result);
} while (result !== sides);

let html = "<ul>";
for (let i = 0; i < rolls.length; i++) {
  html += `<li>${rolls[i]}</li>`;
}
html += "</ul>";

document.body.innerHTML = html;