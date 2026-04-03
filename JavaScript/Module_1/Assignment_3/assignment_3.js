"use strict";
let a = Number(prompt("Enter first number:"));
let b = Number(prompt("Enter second number:"));
let c = Number(prompt("Enter third number:"));

let sum = a + b + c;
let product = a * b * c;
let avg = sum / 3;

document.body.innerHTML = `
Sum: ${sum} <br>
Product: ${product} <br>
Average: ${avg}
`;