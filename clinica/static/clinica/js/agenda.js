// Agenda del día: al elegir una fecha en el calendario, la página cambia sola
const formularioFecha = document.getElementById("form-fecha");
const campoFecha = document.getElementById("ir-fecha");

// Con JavaScript el botón "Ver" ya no hace falta
document.getElementById("boton-ver").hidden = true;

campoFecha.addEventListener("change", () => {
    if (campoFecha.value) {
        formularioFecha.submit();
    }
});
