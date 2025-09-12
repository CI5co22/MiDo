$(document).on("submit", "#agregarMedicina", function (e) {
    // e.preventDefault(); 
    let $form = $(this);
    let recetaId = $form.data("id");

    let nombre = $("#med-name").val();
    let cantidad = $("#med-cantidad").val();
    let cada = $("#med-cada").val();
    let durante = $("#med-durante").val();

    $.ajax({
        url: `/receta/agregar/`, 
        type: "POST",
        data: {
            'nombre': nombre,
            'cantidad': cantidad,
            'cada': cada,
            'durante': durante,
            'recetaId': recetaId,
            'csrfmiddlewaretoken': $form.find("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(resp) {
            if (resp.status === "ok") {
               console.log('Se pudo');
            } else {
                alert("Error al agregar la medicina");
            }
        },
        error: function(xhr, status, error) {
            alert("Error en la solicitud");
        }
    });
});
