document.addEventListener("DOMContentLoaded", function () {
    const valor = document.getElementById("efectividad-valor");
    const btn = document.getElementById("efectividad-btn");

    btn.addEventListener("click", function () {
        if (btn.dataset.mode !== "edit") {
            // --- Cambiar a modo edición ---
            const actual = valor.textContent.trim().split("/")[0];
            valor.innerHTML = `
                <input type="number" min="0" max="10" value="${actual}" 
                    class="efectividad-input me-1" id="efectividad-input" style=" width: 60px;          
    text-align: center;    
    padding: 2px 4px;     
    font-size: 1rem;      
    border: 1px solid #ccc;
    border-radius: 6px;"> /10
            `;

            btn.innerHTML = `<i class="fa-solid fa-check"></i>`;
            btn.dataset.mode = "edit";

        } else {
            const nuevoValor = document.getElementById("efectividad-input").value || 0;
            const recetaId = valor.dataset.efectid;

            fetch(`/actualizar-efectividad/${recetaId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ efectividad: nuevoValor })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    valor.textContent = `${nuevoValor}/10`;
                } else {
                    alert("Error al actualizar");
                }
            })
            .catch(err => console.error(err));

            // Volver al modo view
            btn.innerHTML = `<i class="fa-solid fa-edit"></i>`;
            btn.dataset.mode = "view";
        }
    });
});
