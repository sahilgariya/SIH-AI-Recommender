const form=document.getElementById("recommendationForm");
const submitButton=document.getElementById("submitButton");
const input=document.getElementById("user_input");
const count=document.getElementById("charCount");
const chips=document.querySelectorAll("[data-query]");

function updateCount(){if(count&&input)count.textContent=`${input.value.length}/500`;}
if(input){input.addEventListener("input",updateCount);updateCount();}
chips.forEach(chip=>chip.addEventListener("click",()=>{if(!input)return;input.value=chip.dataset.query||"";updateCount();input.focus();}));
if(form&&submitButton&&input){form.addEventListener("submit",event=>{const value=input.value.trim();if(!value){event.preventDefault();input.focus();return;}if(value.length>500){event.preventDefault();input.focus();return;}submitButton.disabled=true;submitButton.textContent="Analyzing your skills...";});}