const form = document.querySelector("form");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const urlInput = document.querySelector("#url");
  const resultLabel = document.querySelector("#result");
  const response = await fetch("http://localhost:5000/shorten_url", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      url: urlInput.value,
    }),
  });
  const data = await response.json();
  resultLabel.innerText = data.shortened_url;
});
