/* Funcion que valida cada campo y da estilo */
function validarCampo(input, condicion, mensajeError) {
    const mensaje = input.nextElementSibling;

    if (condicion()) {
        mensaje.classList.remove("text-danger");
        mensaje.classList.add("text-success");
        input.classList.remove("is-invalid");
        input.classList.add("is-valid");
        mensaje.textContent = "";
        return true;
    } else {
        mensaje.textContent = mensajeError;
        mensaje.classList.add("text-danger");
        mensaje.classList.remove("text-success");
        input.classList.add("is-invalid");
        input.classList.remove("is-valid");
        return false;
    }
}

/* Función para resetear los estilos de los campos */
function resetCampo(input) {
    const mensaje = input.nextElementSibling;

    input.classList.remove("is-invalid", "is-valid");
    mensaje.textContent = "";
    mensaje.classList.remove("text-danger", "text-success");
}

// VALIDACIÓN TIEMPO REAL CAMPO NOMBRE
const nombreEquipo = document.getElementById("nombreEquipo");

nombreEquipo.addEventListener("input", function () {

    if (nombreEquipo.value.trim().length === 0) {
        resetCampo(nombreEquipo);
        return;
    }

    validarCampo(
        nombreEquipo,
        function () {
            return nombreEquipo.value.trim().length >= 5 && /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(nombreEquipo.value.trim());
        },
        "El nombre debe tener al menos 5 caracteres. No puede contener números ni carácteres especiales."
    );
});

// VALIDACIÓN TIEMPO REAL CAMPO DIRECCIÓN
const direccionEquipo = document.getElementById("direccionEquipo");

direccionEquipo.addEventListener("input", function () {

    if (direccionEquipo.value.trim().length === 0) {
        resetCampo(direccionEquipo);
        return;
    }

    validarCampo(
        direccionEquipo,
        function () {
            return direccionEquipo.value.trim().length >= 10 && /^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s.,ºª\/\-]+$/.test(direccionEquipo.value.trim());
        },
        "La dirección debe tener al menos 10 caracteres. Solo puede contener letras, números y '. , - / º ª'."
    );
});

// VALIDACIÓN TIEMPO REAL CAMPO TELÉFONO
const telefonoEquipo = document.getElementById("telefonoEquipo");

telefonoEquipo.addEventListener("input", () => {
    const valor = telefonoEquipo.value;

    if (valor === "") {
        resetCampo(telefonoEquipo);
        return;
    }

    validarCampo(
        telefonoEquipo,
        () => /^\d{0,9}$/.test(telefonoEquipo.value),
        "Solo se permiten números y como máximo 9 dígitos."
    );
});

// VALIDACIÓN TIEMPO REAL CAMPO AÑO DE FUNDACIÓN
const añoFundaciónEquipo = document.getElementById("anioFundacion");

añoFundaciónEquipo.addEventListener("input", function () {
    let valor = añoFundaciónEquipo.value;
    let mensaje = añoFundaciónEquipo.nextElementSibling;
    if (valor === "") {
        resetCampo(añoFundaciónEquipo);
        return;
    }

    if (añoFundaciónEquipo.value.length > 4) {
        añoFundaciónEquipo.value = añoFundaciónEquipo.value.slice(0, 4);
    }

    const soloNumeros = /^\d+$/.test(valor);

    valor = Number(valor);

    const anioActual = new Date().getFullYear();

    if (soloNumeros && valor >= 1850 && valor <= anioActual) {
        añoFundaciónEquipo.classList.add("is-valid");
        añoFundaciónEquipo.classList.remove("is-invalid");
        mensaje.textContent = "";
    } else {
        añoFundaciónEquipo.classList.add("is-invalid");
        añoFundaciónEquipo.classList.remove("is-valid");
        mensaje.classList.add("text-danger", "text-success");
        mensaje.textContent = "El año de fundación debe ser entre 1850 y " + anioActual + ", ambos inclusive.";
    }
});

// VALIDACIÓN COMPLETA DEL FORMULARIO AL ENVIARLO
const editarEquipoForm = document.getElementById("formulario_editar_datos");

editarEquipoForm.setAttribute("novalidate", true);

editarEquipoForm.addEventListener("submit", function (event) {
    var validarNombre = validarCampo(
        nombreEquipo,
        function () { return nombreEquipo.value.trim().length >= 2 && /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/.test(nombreEquipo.value.trim()); },
        "El nombre debe tener al menos 2 caracteres. No puede contener números ni carácteres especiales."
    );

    var validarDireccion = validarCampo(
        direccionEquipo,
        function () { return direccionEquipo.value.trim().length >= 10 && /^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s.,ºª\/\-]+$/.test(direccionEquipo.value.trim()); },
        "La dirección debe tener al menos 10 caracteres. Solo puede contener letras, números y '. , - / º ª'."
    );

    const validarTelefono = validarCampo(
        telefonoEquipo,
        () => /^\d{9}$/.test(telefonoEquipo.value),
        "El teléfono debe tener exactamente 9 números."
    );

    var validarAño = validarCampo(
        añoFundaciónEquipo,
        function () {
            return añoFundaciónEquipo.value.trim() !== "" && Number(añoFundaciónEquipo.value.trim()) >= 1850 && Number(añoFundaciónEquipo.value.trim()) <= new Date().getFullYear();
        },
        "Año inválido. Debe ser uno entre 1850 y " + new Date().getFullYear() + ", ambos inclusive."
    );

    if (!(
        validarNombre &&
        validarDireccion &&
        validarTelefono &&
        validarAño
    )) {
        event.preventDefault();
    }
});

const msgExito = document.getElementById("modalEditarDatosEquipoOk");

if (msgExito) {
    const modal = new bootstrap.Modal(
        document.getElementById("modalEditarDatosEquipoOk")
    );
    modal.show();
    setTimeout(() => {
        window.location.href = "/"; // o landing
    }, 2500);
}

const msgError = document.getElementById("modalErrorEditarEquipo");

if (msgError) {
    const modal = new bootstrap.Modal(
        document.getElementById("modalErrorEditarEquipo")
    );
    modal.show();
}


const updateModal = document.getElementById('updateProfileModal');

updateModal.addEventListener('hidden.bs.modal', function () {
    const form = updateModal.querySelector('form');
    form.reset();
    resetCampo(nombreEquipo);
    resetCampo(direccionEquipo);
    resetCampo(telefonoEquipo);
    resetCampo(añoFundaciónEquipo);
});