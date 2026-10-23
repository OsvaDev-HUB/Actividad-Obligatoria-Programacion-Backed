// Agendar cita: marca las horas ocupadas y muestra las libres del día elegido
const horasOcupadas = JSON.parse(document.getElementById("horas-ocupadas").textContent);
const campoFecha = document.getElementById("id_fecha");
const campoHora = document.getElementById("id_hora");
const listaHoras = document.getElementById("lista-horas");
const diaElegido = document.getElementById("dia-elegido");

// Fecha y hora del servidor, para no depender del reloj del computador
const hoy = listaHoras.dataset.hoy;
const ahora = listaHoras.dataset.ahora;

function nombreDelDia(fecha) {
    // "2026-10-23" -> "viernes 23 de octubre"
    const dia = new Date(fecha + "T00:00");
    const semana = dia.toLocaleDateString("es-CL", { weekday: "long" });
    const mes = dia.toLocaleDateString("es-CL", { month: "long" });
    return `${semana} ${dia.getDate()} de ${mes}`;
}

function actualizarHoras() {
    const fecha = campoFecha.value;
    const tomadas = horasOcupadas[fecha] || [];
    listaHoras.innerHTML = "";

    if (!fecha || fecha < hoy) {
        diaElegido.textContent = "Elige una fecha desde hoy para ver sus horas.";
        return;
    }

    let libres = 0;
    for (const opcion of campoHora.options) {
        const hora = opcion.value;
        const ocupada = tomadas.includes(hora);
        const yaPaso = fecha === hoy && hora <= ahora;

        // En el selector, las horas que no se pueden elegir quedan deshabilitadas
        opcion.disabled = ocupada || yaPaso;
        opcion.textContent = ocupada ? hora + " (ocupada)" : yaPaso ? hora + " (ya pasó)" : hora;

        if (!opcion.disabled) {
            libres++;
            // Cada hora libre es un botón que la elige en el selector
            const boton = document.createElement("button");
            boton.type = "button";
            boton.className = "ficha-hora";
            boton.textContent = hora;
            boton.setAttribute("aria-pressed", campoHora.value === hora ? "true" : "false");
            boton.addEventListener("click", () => {
                campoHora.value = hora;
                marcarElegida();
            });
            const item = document.createElement("li");
            item.appendChild(boton);
            listaHoras.appendChild(item);
        }
    }

    // Si la hora elegida quedó ocupada, se pasa a la primera libre
    if (campoHora.selectedOptions[0] && campoHora.selectedOptions[0].disabled) {
        const primeraLibre = [...campoHora.options].find((opcion) => !opcion.disabled);
        campoHora.value = primeraLibre ? primeraLibre.value : "";
        marcarElegida();
    }

    const texto = nombreDelDia(fecha);
    diaElegido.textContent = libres
        ? `${libres} hora${libres === 1 ? "" : "s"} libre${libres === 1 ? "" : "s"} el ${texto}.`
        : `No quedan horas libres el ${texto}.`;
}

function marcarElegida() {
    for (const boton of listaHoras.querySelectorAll("button")) {
        boton.setAttribute("aria-pressed", boton.textContent === campoHora.value ? "true" : "false");
    }
}

campoFecha.addEventListener("change", actualizarHoras);
campoHora.addEventListener("change", marcarElegida);
actualizarHoras();
