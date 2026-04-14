const form = document.getElementById("searchForm");
const input = document.getElementById("query");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const value = input.value.trim();

  if (!value) return;

  try {
    const response = await fetch(
      `https://api.chucknorris.io/jokes/search?query=${value}`
    );

    const data = await response.json();

    resultsDiv.innerHTML = "";

    data.result.forEach(jokeItem => {
      const article = document.createElement("article");

      const p = document.createElement("p");
      p.textContent = jokeItem.value;

      article.appendChild(p);
      resultsDiv.appendChild(article);
    });

  } catch (error) {
    console.error("Error fetching jokes:", error);
  }
});