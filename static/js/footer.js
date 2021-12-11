const currentYear = document.querySelector(".current__year__footer");

const date = new Date();

currentYear.textContent = date.getFullYear();