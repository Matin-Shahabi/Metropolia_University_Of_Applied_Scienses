const form = document.getElementById("searchForm");
const input = document.getElementById("query");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const value = input.value.trim();

  if (!value) return;

  try {
    const response = await fetch(`https://api.tvmaze.com/search/shows?q=${value}`);
    const data = await response.json();

    resultsDiv.innerHTML = "";

    data.forEach(tvShow => {
      const show = tvShow.show;

      const article = document.createElement("article");

      const h2 = document.createElement("h2");
      h2.textContent = show.name;

      const link = document.createElement("a");
      link.href = show.url;
      link.target = "_blank";
      link.textContent = "More details";

      const img = document.createElement("img");
      img.src = show.image
        ? show.image.medium
        : "https://placehold.co/210x295?text=Not%20Found";
      img.alt = show.name;

      const summary = document.createElement("div");
      summary.innerHTML = show.summary || "No summary available";

      article.appendChild(h2);
      article.appendChild(link);
      article.appendChild(document.createElement("br"));
      article.appendChild(img);
      article.appendChild(summary);

      resultsDiv.appendChild(article);
    });

  } catch (error) {
    console.error("Error fetching data:", error);
  }
});