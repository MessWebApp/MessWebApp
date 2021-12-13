const reviewBox = document.querySelector(".review__box");

const closeButton = document.querySelector(".cross");
const reviewButton = document.querySelectorAll(".review__button");
const overlay = document.querySelector(".overlay");

reviewButton.forEach((btn) =>{
  btn.addEventListener("click", ()=>{
    reviewBox.classList.toggle("show-review")
    overlay.classList.toggle("show-overlay");
  })
})

closeButton.addEventListener("click", ()=>{
  reviewBox.classList.toggle("show-review");
  overlay.classList.toggle("show-overlay");
});