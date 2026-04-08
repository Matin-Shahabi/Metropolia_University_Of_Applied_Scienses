"use strict";
let count = Number(prompt("Enter number of participants:"));
let names = [];

for (let i = 0; i < count; i++) {
  let name = prompt(`Enter name ${i}:`);
  names.push(name);
}

names.sort();

let html = "<ol>";

for (let i = 0; i < names.length; i++) {
  html += `<li>${names[i]}</li>`;
}

html += "</ol>";

document.body.innerHTML = html;