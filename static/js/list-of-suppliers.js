const acceptDeclinedStatus = document.querySelectorAll(".accept__declined__status");
const form_submit = document.querySelectorAll('.submit_form');
const declinedModel = document.querySelector(".declined__model");
const declinedModelCloseBtn = document.querySelector(".declined__model__close");
const viewAddharBtn = document.querySelectorAll(".view__addhar");
const addharModel = document.querySelector(".addhar__model");
const addharCloseBtn = document.querySelector(".addhar__closed__btn");
const overlay = document.querySelector(".overlay");
const iframe_model = document.querySelector('.iframe_model');

acceptDeclinedStatus.forEach((select,index)=>{
  select.addEventListener("change", (e)=>
  {
    if(e.target.value !== 'panding')
    {
      form_submit[index].submit();
    }
  })
});


viewAddharBtn.forEach((btn,index)=>
{
  btn.addEventListener("click", ()=>
  {
     let url = btn.getAttribute('data-url');
     iframe_model.src = url;
     addharModel.classList.toggle("show-addhar-model");
     overlay.classList.toggle("show-overlay");

  });
});

addharCloseBtn.addEventListener("click", ()=>{
  addharModel.classList.toggle("show-addhar-model");
  overlay.classList.toggle("show-overlay");

});


declinedModelCloseBtn.addEventListener("click", ()=>{
  declinedModel.classList.toggle("display-declined-model");
  overlay.classList.toggle("show-overlay");

});


