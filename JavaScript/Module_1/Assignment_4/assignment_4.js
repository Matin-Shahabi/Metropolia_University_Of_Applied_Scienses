"use strict";
let name = prompt("Enter your name:");
let houseNumber = Math.floor(Math.random() * 4) + 1;

let house;

switch (houseNumber) {
  case 1:
    house = "Gryffindor";
    break;
  case 2:
    house = "Slytherin";
    break;
  case 3:
    house = "Hufflepuff";
    break;
  case 4:
    house = "Ravenclaw";
    break;
}

document.body.innerHTML = `${name}, you are ${house}.`;