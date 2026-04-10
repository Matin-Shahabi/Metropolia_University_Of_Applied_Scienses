const form = document.querySelector('form');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const firstName = document.querySelector('input[name="firstname"]').value;
  const lastName = document.querySelector('input[name="lastname"]').value;

  document.getElementById('target').textContent =
    `Your name is ${firstName} ${lastName}`;
});