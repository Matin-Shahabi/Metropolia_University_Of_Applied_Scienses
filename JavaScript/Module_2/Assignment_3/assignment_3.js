"use strict";
let dogs = [];

for (let i = 0; i < 6; i++) {
  let name = prompt(`Enter dog ${i} name:`);
  dogs.push(name);
}

dogs.sort();
dogs.reverse();

let html = "<ul>";

for (let i = 0; i < dogs.length; i++) {
  html += `<li>${dogs[i]}</li>`;
}

html += "</ul>";

document.body.innerHTML = html;