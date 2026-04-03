"use strict";
let diceCount = Number(prompt("Number of dice:"));
let targetSum = Number(prompt("Target sum:"));

let simulations = 10000;
let success = 0;

for (let i = 0; i < simulations; i++) {
  let sum = 0;

  for (let j = 0; j < diceCount; j++) {
    sum += Math.floor(Math.random() * 6) + 1;
  }

  if (sum === targetSum) {
    success++;
  }
}

let probability = (success / simulations) * 100;

document.body.innerHTML =
  `Probability to get sum ${targetSum} with ${diceCount} dice is ${probability.toFixed(2)}%`;