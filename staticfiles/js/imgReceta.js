document.addEventListener("click", function(e) {
  if (e.target.closest(".ver")) {
    let btn = e.target.closest(".ver");
    let imgUrl = btn.getAttribute("data-img");
    document.getElementById("imgMedicamento").src = imgUrl;
  }
});
