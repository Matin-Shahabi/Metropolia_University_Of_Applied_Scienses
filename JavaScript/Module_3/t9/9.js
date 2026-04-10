const btn = document.querySelector('button');

btn.addEventListener('click', () => {
  const input = document.getElementById('calculation').value;

  let operator;

  if (input.includes('+')) operator = '+';
  else if (input.includes('-')) operator = '-';
  else if (input.includes('*')) operator = '*';
  else if (input.includes('/')) operator = '/';

  const parts = input.split(operator);
  const num1 = Number(parts[0]);
  const num2 = Number(parts[1]);

  let result;

  if (operator === '+') result = num1 + num2;
  else if (operator === '-') result = num1 - num2;
  else if (operator === '*') result = num1 * num2;
  else if (operator === '/') result = num1 / num2;

  document.getElementById('result').textContent = result;
});