const trigger = document.getElementById('trigger');
const img = document.getElementById('target');

trigger.addEventListener('mouseover', () => {
  img.src = 'img/picB.jpg';
});

trigger.addEventListener('mouseout', () => {
  img.src = 'img/picA.jpg';
});