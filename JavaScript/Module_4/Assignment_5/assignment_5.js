async function getJoke() {
  try {
    const response = await fetch("https://api.chucknorris.io/jokes/random");
    const data = await response.json();

    console.log(data.value);
  } catch (error) {
    console.error("Error fetching joke:", error);
  }
}

getJoke();