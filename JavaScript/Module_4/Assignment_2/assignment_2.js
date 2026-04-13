"use strict";
const form = document.getElementById("searchForm");
const input = document.getElementById("query");

form.addEventListener("submit", async (event) => {
  event.preventDefault(); // stop page reload

  const value = input.value.trim();

  if (!value) {
    console.log("Please enter a search term.");
    return;
  }

  try {
    const response = await fetch(`https://api.tvmaze.com/search/shows?q=${value}`);
    const data = await response.json();

    console.log("Search result:", data);

  } catch (error) {
    console.error("Error fetching data:", error);
  }
});