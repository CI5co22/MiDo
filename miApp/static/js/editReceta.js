const Modal = document.getElementById('editarRecetaModal')
Modal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget

    const id = button.getAttribute('data-id')
    const doc = button.getAttribute('data-doc')
    const lugar = button.getAttribute('data-lugar')
    const fecha = button.getAttribute('data-fecha')
 
    Modal.querySelector('#recetaID').value = id
    Modal.querySelector('#doc').value = doc
    Modal.querySelector('#lugar').value = lugar
    Modal.querySelector('#fecha').value = fecha
 
})