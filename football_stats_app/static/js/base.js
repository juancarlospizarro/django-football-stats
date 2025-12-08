document.getElementById("anio_actual").innerHTML = new Date().getFullYear();
const html = document.documentElement;
    const button = document.getElementById("themeToggle");

    // Cargar tema guardado
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        html.setAttribute("data-bs-theme", savedTheme);
        updateButton(savedTheme);
    }

    button.addEventListener("click", () => {
        const newTheme = html.getAttribute("data-bs-theme") === "light" ? "dark" : "light";
        
        html.setAttribute("data-bs-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateButton(newTheme);
    });

    function updateButton(theme) {
        button.innerHTML = theme === "dark" ? "☀️ Modo claro" : "🌙 Modo oscuro";
    }