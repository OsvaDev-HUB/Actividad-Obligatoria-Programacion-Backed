// Actualiza la placa de vista previa mientras se llena el formulario de nuevo paciente
const placa = document.getElementById("placa-previa");
const campoNombre = document.getElementById("id_nombre");
const campoDueno = document.getElementById("id_nombre_dueno");
const opcionesEspecie = document.querySelectorAll('input[name="especie"]');

function actualizarPlaca() {
    const nombre = campoNombre.value.trim();
    const dueno = campoDueno.value.trim();
    const elegida = document.querySelector('input[name="especie"]:checked');

    document.getElementById("placa-nombre").textContent = nombre || "Nombre";
    document.getElementById("placa-dueno").textContent = dueno || "Dueño";

    // El color de la placa cambia según la especie elegida
    placa.className = "placa placa--grande";
    if (elegida) {
        placa.classList.add("placa--" + elegida.value);
        document.getElementById("placa-especie").textContent = elegida.parentElement.textContent.trim();
    } else {
        document.getElementById("placa-especie").textContent = "Especie";
    }
    placa.classList.toggle("placa--vacia", !nombre);
}

campoNombre.addEventListener("input", actualizarPlaca);
campoDueno.addEventListener("input", actualizarPlaca);
opcionesEspecie.forEach((opcion) => opcion.addEventListener("change", actualizarPlaca));
actualizarPlaca();
