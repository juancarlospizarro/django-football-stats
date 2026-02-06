document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('themeToggle');

    // Restaurar tema guardado
    if (localStorage.getItem('dark-mode') === 'true') {
        document.body.classList.add('dark-mode');
    }

    // Actualizar botón solo si existe
    if (btn) {
        function updateButton() {
            const isDark = document.body.classList.contains('dark-mode');
            btn.innerHTML = isDark ? "☀️" : "🌙";
        }

        updateButton();

        btn.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('dark-mode', document.body.classList.contains('dark-mode'));
            updateButton();
        });
    }

    // Actualizar año actual si existe
    const anio = document.getElementById("anio_actual");
    if (anio) anio.innerHTML = new Date().getFullYear();
});