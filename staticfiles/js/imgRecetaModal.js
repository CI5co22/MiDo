const modal = document.getElementById('modalMedicamento');

modal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    const imgUrl = button.getAttribute('data-img');
    const img = modal.querySelector('#imgMedicamento');
    const noText = modal.querySelector('#noImageText');

    // Verifica que sea una URL válida y que no sea "default.png" (si usas imagen por defecto)
    if (imgUrl && imgUrl.trim() !== '' && !imgUrl.includes('default.png')) {
        img.src = imgUrl;
        img.style.display = 'block';
        noText.style.display = 'none';
    } else {
        img.src = ''; // limpia src por si acaso
        img.style.display = 'none';
        noText.style.display = 'block';
    }
});