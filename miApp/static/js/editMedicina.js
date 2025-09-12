const editModal = document.getElementById('editModal')
editModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget

    const recetaID = button.getAttribute('data-receta_id')
    const id = button.getAttribute('data-id')
    const nombre = button.getAttribute('data-title')
    const cantidad = button.getAttribute('data-cantidad')
    const cada = button.getAttribute('data-cada')
    const durante = button.getAttribute('data-durante')
    
    editModal.querySelector('#edit-id').value = id
    editModal.querySelector('#edit-title').value = nombre
    editModal.querySelector('#edit-cantidad').value = cantidad
    editModal.querySelector('#edit-cada').value = cada
    editModal.querySelector('#edit-durante').value = durante
    editModal.querySelector('#recetaID').value = recetaID
})