const acceptDeclinedStatus = document.querySelectorAll(".accept__declined__status");
const declinedModel = document.querySelector(".declined__model");
const declinedModelCloseBtn = document.querySelector(".declined__model__close");
const viewAddharBtn = document.querySelectorAll(".view__addhar");
const addharModel = document.querySelector(".addhar__model");
const addharCloseBtn = document.querySelector(".addhar__closed__btn");
const overlay = document.querySelector(".overlay");

acceptDeclinedStatus.forEach((select)=>{
  select.addEventListener("change", ()=>{
    if(select.value == "declined")
    {
      declinedModel.classList.toggle("display-declined-model");
        overlay.classList.toggle("show-overlay");

    }
  })
});


declinedModelCloseBtn.addEventListener("click", ()=>{
  declinedModel.classList.toggle("display-declined-model");
  overlay.classList.toggle("show-overlay");

});

viewAddharBtn.forEach((btn)=>{
  btn.addEventListener("click", ()=>{
     addharModel.classList.toggle("show-addhar-model");
     overlay.classList.toggle("show-overlay");

  });
});

addharCloseBtn.addEventListener("click", ()=>{
  addharModel.classList.toggle("show-addhar-model");
  overlay.classList.toggle("show-overlay");

});

