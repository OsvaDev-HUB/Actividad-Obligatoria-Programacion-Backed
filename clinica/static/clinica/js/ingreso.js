// Ayudas del formulario de ingreso del personal
const formulario = document.getElementById("form-ingreso");
const campoClave = document.getElementById("id_password");
const botonMostrar = document.getElementById("mostrar-clave");
const avisoMayus = document.getElementById("aviso-mayus");
const botonIngresar = document.getElementById("boton-ingresar");

// Botón "Mostrar": cambia la contraseña entre oculta y visible
botonMostrar.hidden = false;
botonMostrar.addEventListener("click", () => {
    const oculta = campoClave.type === "password";
    campoClave.type = oculta ? "text" : "password";
    botonMostrar.textContent = oculta ? "Ocultar" : "Mostrar";
    campoClave.focus();
});

// Aviso cuando Bloq Mayús está activado mientras se escribe la contraseña
function revisarMayus(evento) {
    if (evento.getModifierState) {
        avisoMayus.hidden = !evento.getModifierState("CapsLock");
    }
}
campoClave.addEventListener("keydown", revisarMayus);
campoClave.addEventListener("keyup", revisarMayus);
campoClave.addEventListener("blur", () => {
    avisoMayus.hidden = true;
});

// Al enviar, el botón muestra que está trabajando y evita el doble clic
formulario.addEventListener("submit", () => {
    botonIngresar.disabled = true;
    botonIngresar.textContent = "Ingresando…";
    // La contraseña vuelve a quedar oculta antes de enviar
    campoClave.type = "password";
});

// Si se vuelve a esta página con el botón "Atrás", el botón queda usable otra vez
window.addEventListener("pageshow", () => {
    botonIngresar.disabled = false;
    botonIngresar.textContent = "Ingresar";
});
