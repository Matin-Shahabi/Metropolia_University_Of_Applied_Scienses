"use strict";
let year = Number(prompt("Enter a year:"));

let isLeap = false;

if (year % 4 === 0) {
  if (year % 100 === 0) {
    if (year % 400 === 0) {
      isLeap = true;
    }
  } else {
    isLeap = true;
  }
}

document.body.innerHTML = isLeap
  ? `${year} is a leap year`
  : `${year} is not a leap year`;