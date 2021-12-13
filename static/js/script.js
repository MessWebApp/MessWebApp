var swiper = new Swiper(".mySwiper", {
    slidesPerView: 4,
    spaceBetween: 20,
    slidesPerGroup: 3,
    loop: true,
    loopFillGroupWithBlank: true,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });
// // ======= active link =======
// const menuLinks = document.querySelectorAll(".menu .list-item a");

// const linkAction = ()=>{
//     menuLinks.forEach((link)=>{
//         link.classList.remove("active");
//         this.classList.add("active");
//     });    
// }

// navLink.forEach(link => link.addEventListener("click", linkAction));

const authBtn = document.querySelector(".auth__container");

// models
const authenticationModel = document.querySelector(".authentication__model");
const customerAuthenticationModel = document.querySelector(".customer__authentication__model");
const supplierAuthenticationModel = document.querySelector(".supplier__authentication__model");

// models links
const customerAuthLink = document.querySelector(".customer__auth__link");
const supplierAuthLink = document.querySelector(".supplier__auth__link");

const customerLoginLink = document.querySelector(".customer__login__link");
const customerRegisterLink = document.querySelector(".customer__register__link");

const supplierLoginLink = document.querySelector(".supplier__login__link");
const supplierRegisterLink = document.querySelector(".supplier__register__link");

// black layer
const blackLayer = document.querySelector(".black__layer");


authBtn.addEventListener("click", ()=>{
    authenticationModel.classList.toggle("show__model");
    customerAuthenticationModel.classList.remove("show__model");
    supplierAuthenticationModel.classList.remove("show__model");

    blackLayer.classList.toggle("show__layer");
});

supplierAuthLink.addEventListener("click", ()=>{
    supplierAuthenticationModel.classList.toggle("show__model");
    customerAuthenticationModel.classList.remove("show__model");
});

customerAuthLink.addEventListener("click", ()=>{
    customerAuthenticationModel.classList.toggle("show__model");
    supplierAuthenticationModel.classList.remove("show__model");

})