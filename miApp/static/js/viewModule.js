let pilas = document.getElementById("pilas");
let grid = document.getElementById("grid");

pilas.addEventListener("click", event =>
{
    pilas.classList.remove("no-select");
    grid.classList.add("no-select")
}
)

grid.addEventListener("click", event =>
{
    grid.classList.remove("no-select");
    pilas.classList.add("no-select")
}
)
