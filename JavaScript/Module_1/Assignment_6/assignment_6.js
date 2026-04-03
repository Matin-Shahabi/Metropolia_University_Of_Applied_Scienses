"use strict";
let answer = confirm("Should I calculate the square root?");

if (answer) {
  let num = Number(prompt("Enter a number:"));

  if (num < 0) {
    document.body.innerHTML = "The square root of a negative number is not defined";
  } else {
    document.body.innerHTML = `Square root is ${Math.sqrt(num)}`;
  }
} else {
  document.body.innerHTML = "The square root is not calculated.";
}