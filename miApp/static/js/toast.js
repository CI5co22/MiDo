document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('toast-container');

    const messagesScript = document.getElementById('messages-data'); 
    const messages = messagesScript ? JSON.parse(messagesScript.textContent) : [];


    messages.forEach(msg => createToast(msg));

    function createToast(msg) {
        const toast = document.createElement('div');
        toast.classList.add('toast-custom');

        toast.innerHTML = `
            <i class="fa-solid fa-check me-1" style="color:green" ></i>
            ${msg}
            <button class="close-btn">&times;</button>
        `;

        container.appendChild(toast);


        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => container.removeChild(toast), 500);
        }, 3500);

        toast.querySelector('.close-btn').addEventListener('click', () => {
            toast.classList.remove('show');
            setTimeout(() => container.removeChild(toast), 500);
        });
    }
});
