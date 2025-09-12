$(document).on("submit", "#agregarMedicina", function (e) {

    let $form = $(this);
    let recetaId = $form.data("id");

    let formData = new FormData($form[0]);
    formData.append("recetaId", recetaId);

    $.ajax({
        url: `/receta/agregar/`,
        type: "POST",
        data: formData,
        processData: false,  
        contentType: false,   
        success: function(resp) {
            if (resp.status === "ok") {
                console.log("Se pudo");
            } else {
                alert("Error al agregar la medicina");
            }
        },
        error: function(xhr, status, error) {
            alert("Error en la solicitud");
        }
    });
});
