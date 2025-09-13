document.querySelectorAll('.receta').forEach(div => {
    div.addEventListener("click", function() {
        let id = this.getAttribute("data-id");
        window.location.href = "/receta/" + id + "/"; 
    });
});

