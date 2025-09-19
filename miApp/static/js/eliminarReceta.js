document.addEventListener('DOMContentLoaded', function() {
    let formToSubmit = null;

    const deleteButtons = document.querySelectorAll('.btn.eliminar');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();

            const formId = this.nextElementSibling.id;
            formToSubmit = document.getElementById(formId);

            const modal = document.getElementById('confirm-modal');
            document.getElementById('confirm-message').textContent = "¿Estás seguro de que deseas eliminar esta receta?";
            modal.style.display = 'flex';
        });
    });

    document.getElementById('confirm-yes').addEventListener('click', function() {
        if(formToSubmit) formToSubmit.submit();
        document.getElementById('confirm-modal').style.display = 'none';
    });
    
    document.getElementById('confirm-no').addEventListener('click', function() {
        formToSubmit = null;
        document.getElementById('confirm-modal').style.display = 'none';
    });
});
