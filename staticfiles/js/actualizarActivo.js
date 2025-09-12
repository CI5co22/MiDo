elemento = document.getElementById('switchCheckDefault');


elemento.addEventListener("click", function() {
    let id = this.getAttribute("data-id");
    const token = this.getAttribute("data-token");

    $.ajax({
        url: `/receta/activar/`, 
        type: "POST",
        data: {
            'id': id,
            'csrfmiddlewaretoken': token
        },
        success: function(resp) {
            if (resp.status === "ok") {
               console.log('Se actualizo correctamente');
            } else {
                alert("Error al cambiar");
            }
        },
        error: function(xhr, status, error) {
            alert("Error en la solicitud");
        }
    });
});


