// Arma la ficha del paciente mientras se llena el formulario de nuevo paciente
const ficha = document.getElementById("ficha");
const foto = document.getElementById("ficha-foto");
const imagen = document.getElementById("ficha-imagen");
const inicial = document.getElementById("ficha-inicial");
const campoNombre = document.getElementById("id_nombre");
const campoDueno = document.getElementById("id_nombre_dueno");
const opcionesEspecie = document.querySelectorAll('input[name="especie"]');

function actualizarFicha() {
    const nombre = campoNombre.value.trim();
    const dueno = campoDueno.value.trim();
    const elegida = document.querySelector('input[name="especie"]:checked');

    document.getElementById("ficha-nombre").textContent = nombre || "Nombre";
    document.getElementById("ficha-dueno").textContent = dueno || "Sin nombre";
    inicial.textContent = nombre ? nombre.charAt(0).toUpperCase() : "?";
    ficha.classList.toggle("ficha--vacia", !nombre);

    // La especie cambia los colores de la ficha y muestra su foto
    ficha.className = ficha.className.replace(/especie-\S+/g, "").trim();
    if (elegida) {
        ficha.classList.add("especie-" + elegida.value);
        imagen.src = elegida.dataset.foto;
        imagen.hidden = false;
        foto.classList.remove("ficha__foto--vacia");
        document.getElementById("ficha-especie").textContent = elegida.parentElement.textContent.trim();
    } else {
        imagen.hidden = true;
        foto.classList.add("ficha__foto--vacia");
        document.getElementById("ficha-especie").textContent = "Sin especie";
    }
}

campoNombre.addEventListener("input", actualizarFicha);
campoDueno.addEventListener("input", actualizarFicha);
opcionesEspecie.forEach((opcion) => opcion.addEventListener("change", actualizarFicha));
actualizarFicha();
