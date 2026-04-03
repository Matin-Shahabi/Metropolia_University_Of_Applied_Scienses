"use strict";
let num = Number(prompt("Enter a number:"));
let isPrime = true;

if (num < 2) isPrime = false;

for (let i = 2; i < num; i++) {
  if (num % i === 0) {
    isPrime = false;
    break;
  }
}

document.body.innerHTML = isPrime
  ? `${num} is prime`
  : `${num} is not prime`;