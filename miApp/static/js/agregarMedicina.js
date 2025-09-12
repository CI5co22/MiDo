$(document).on("submit", "#agregarMedicina", function (e) {
    e.preventDefault(); // 👈 ahora sí, para que no recargue el form
    
    let $form = $(this);
    let recetaId = $form.data("id");

    // creamos el FormData con todos los campos del formulario
    let formData = new FormData($form[0]);
    formData.append("recetaId", recetaId);

    $.ajax({
        url: `/receta/agregar/`,
        type: "POST",
        data: formData,
        processData: false,   // 👈 obligatorio con FormData
        contentType: false,   // 👈 obligatorio con FormData
        success: function(resp) {
            if (resp.status === "ok") {
                console.log("Se pudo");
                // aquí podrías cerrar el modal y refrescar tu tabla sin recargar toda la página
                $("#exampleModal").modal("hide");
            } else {
                alert("Error al agregar la medicina");
            }
        },
        error: function(xhr, status, error) {
            alert("Error en la solicitud");
        }
    });
});
