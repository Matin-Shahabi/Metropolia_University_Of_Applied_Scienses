"use strict";
function even(arr) {
  let result = [];

  for (let i = 0; i < arr.length; i++) {
    if (arr[i] % 2 === 0) {
      result.push(arr[i]);
    }
  }

  return result;
}

let numbers = [2, 7, 4];

let evens = even(numbers);

console.log("Original:", numbers);
console.log("Even:", evens);