$(document).on("submit", "#agregarMedicina", function (e) {   
    let $form = $(this);
    let recetaId = $form.data("id");

    let formData = new FormData($form[0]);
    formData.append("recetaId", recetaId);
    formData.append("csrfmiddlewaretoken", $form.find("input[name='csrfmiddlewaretoken']").val());

    // Mostrar spinner
    $("#spinner").show();

    $.ajax({
        url: `/receta/agregar/`,
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(resp) {
            $("#spinner").hide(); // Ocultar spinner
            if (resp.status === "ok") {
                $('#exampleModal').modal('hide');
                location.reload();
            } else {
                alert("Error al agregar la medicina");
            }
        },
        error: function(xhr, status, error) {
            $("#spinner").hide(); // Ocultar spinner
            alert("Error en la solicitud");
        }
    });

});
