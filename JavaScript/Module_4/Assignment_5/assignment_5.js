async function getJoke() {
  try {
    const response = await fetch("https://api.chucknorris.io/jokes/random");
    const data = await response.json();

    console.log(data.value); // only the joke text
  } catch (error) {
    console.error("Error fetching joke:", error);
  }
}

getJoke();