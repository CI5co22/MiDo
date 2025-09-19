let pilas = document.getElementById("pilas");
let grid = document.getElementById("grid");
let recetas = document.querySelectorAll(".receta")
let contenedor = document.querySelectorAll(".recetas")

const viewModule = localStorage.getItem("view")
console.log(viewModule)


if(viewModule == "grid")
{
    Grid()
}
else
{
    Pilas()
}

pilas.addEventListener("click", event =>
{
    Pilas();
})

grid.addEventListener("click", event =>
{
    Grid()
}
)

function Pilas()
{
    pilas.classList.remove("no-select");
    grid.classList.add("no-select")
    recetas.forEach(element => {
        element.classList.remove("receta-grid")
    });
    contenedor.forEach(element => {
        element.style.display = ""
        element.style.flexWrap = "nowrap"
        element.classList.remove("recetas-grid")
    });
    
    localStorage.setItem("view",'pilas')
}

function Grid()
{
    grid.classList.remove("no-select");
    pilas.classList.add("no-select")
    recetas.forEach(element => {
        element.classList.add("receta-grid")
        element.style.marginRight = "10px"
    });
       contenedor.forEach(e => {
        e.style.display = "flex"
        e.style.flexWrap = "wrap"
        e.classList.add("recetas-grid")
    });
    localStorage.setItem("view",'grid')
}
