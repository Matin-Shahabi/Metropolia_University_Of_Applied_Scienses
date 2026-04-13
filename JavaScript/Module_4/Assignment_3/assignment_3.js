const form = document.getElementById("searchForm");
const input = document.getElementById("query");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const value = input.value.trim();

  if (!value) {
    console.log("Please enter a search term");
    return;
  }

  try {
    const response = await fetch(`https://api.tvmaze.com/search/shows?q=${value}`);
    const data = await response.json();

    // Clear previous results
    resultsDiv.innerHTML = "";

    data.forEach(tvShow => {
      const show = tvShow.show;

      // Create article
      const article = document.createElement("article");

      // Name (h2)
      const h2 = document.createElement("h2");
      h2.textContent = show.name;

      // URL (a)
      const link = document.createElement("a");
      link.href = show.url;
      link.target = "_blank";
      link.textContent = "More details";

      // Image (optional chaining used)
      const img = document.createElement("img");
      img.src = show.image?.medium || "";
      img.alt = show.name;

      // Summary (div)
      const summary = document.createElement("div");
      summary.innerHTML = show.summary || "No summary available";

      // Append elements to article
      article.appendChild(h2);
      article.appendChild(link);
      article.appendChild(document.createElement("br"));
      article.appendChild(img);
      article.appendChild(summary);

      // Append article to results
      resultsDiv.appendChild(article);
    });

  } catch (error) {
    console.error("Error fetching data:", error);
  }
});