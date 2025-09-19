
    let elemento = document.getElementById('cbx-3');

    if (elemento) {
        elemento.addEventListener("click", function() {
            let id = this.getAttribute("data-id");
            let token = this.getAttribute("data-token");

            $.ajax({
                url: `/receta/activar/`, 
                type: "POST",
                data: {
                    'id': id,
                    'csrfmiddlewaretoken': token
                },
                success: function(resp) {
                    if (resp.status === "ok") {
                        console.log('Se actualizó correctamente');
                    } else {
                        alert("Error al cambiar");
                    }
                },
                error: function() {
                    alert("Error en la solicitud");
                }
            });
        });
    }

