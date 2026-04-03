"use strict";
let start = Number(prompt("Start year:"));
let end = Number(prompt("End year:"));

let html = "<ul>";

for (let y = start; y <= end; y++) {
  if ((y % 4 === 0 && y % 100 !== 0) || (y % 400 === 0)) {
    html += `<li>${y}</li>`;
  }
}

html += "</ul>";

document.body.innerHTML = html;