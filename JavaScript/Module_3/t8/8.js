const button = document.getElementById("start")

button.addEventListener('click', (e) => {
  e.preventDefault();

  const num1 = Number(document.getElementById('num1').value);
  const num2 = Number(document.getElementById('num2').value);
  const operation = document.getElementById('operation').value;

  let result;

  if (operation === 'add') {
    result = num1 + num2;
  }
  else if (operation === 'sub') {
    result = num1 - num2;
  }
  else if (operation === 'multi') {
    result = num1 * num2;
  }
  else if (operation === 'div') {
    result = num1 / num2;
  }

  document.getElementById('result').textContent = result;
});