$(document).on("submit", "#agregarMedicina", function (e) {
    let $form = $(this);
    let recetaId = $form.data("id");

    let formData = new FormData($form[0]);
    formData.append("recetaId", recetaId);


    formData.append("csrfmiddlewaretoken", $form.find("input[name='csrfmiddlewaretoken']").val());

    $.ajax({
        url: `/receta/agregar/`,
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(resp) {
            if (resp.status === "ok") {
                // Cierra el modal
                $('#exampleModal').modal('hide');
              
                location.reload();
            } else {
                alert("Error al agregar la medicina");
            }
        },
        error: function(xhr, status, error) {
            alert("Error en la solicitud");
        }
    });

    return false; 
});
