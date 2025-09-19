let pilas = document.getElementById("pilas");
let grid = document.getElementById("grid");
let recetas = document.querySelectorAll(".receta")
let contenedor = document.querySelectorAll(".recetas")

const viewModule = localStorage.getItem("view")
console.log(viewModule)

if(viewModule == "grid")
{
    grid.classList.remove("no-select");
    pilas.classList.add("no-select")
    recetas.forEach(element => {
        element.classList.add("receta-grid")
        element.style.marginRight = "10px"
    });
    contenedor.forEach(element => {
        element.style.display = "flex"
    });
}
else
{
    pilas.classList.remove("no-select");
    grid.classList.add("no-select")
    recetas.forEach(element => {
        element.classList.remove("receta-grid")
    });
    contenedor.forEach(element => {
        element.style.display = ""
    });
}

pilas.addEventListener("click", event =>
{
    pilas.classList.remove("no-select");
    grid.classList.add("no-select")
    recetas.forEach(element => {
        element.classList.remove("receta-grid")
    });
    contenedor.forEach(element => {
        element.style.display = ""
    });

    localStorage.setItem("view",'pilas')
}
)

grid.addEventListener("click", event =>
{
    grid.classList.remove("no-select");
    pilas.classList.add("no-select")
    recetas.forEach(element => {
        element.classList.add("receta-grid")
        element.style.marginRight = "10px"
    });
    contenedor.forEach(element => {
        element.style.display = "flex"
    });
    localStorage.setItem("view",'grid')
}
)
