"use strict";
function rollDice() {
  return Math.floor(Math.random() * 6) + 1;
}

let rolls = [];
let result;

do {
  result = rollDice();
  rolls.push(result);
} while (result !== 6);

let html = "<ul>";
for (let i = 0; i < rolls.length; i++) {
  html += `<li>${rolls[i]}</li>`;
}
html += "</ul>";

document.body.innerHTML = html;