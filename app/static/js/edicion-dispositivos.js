let modoEdicion = false;

document.addEventListener('DOMContentLoaded', () => {
  const boton = document.getElementById('toggle-edicion');
  if (!boton) return;

  boton.addEventListener('click', () => {
    modoEdicion = !modoEdicion;
    const inputs = document.querySelectorAll('input, select');
    const guardarBtns = document.querySelectorAll('.guardar-btn');

    inputs.forEach(i => i.disabled = !modoEdicion);
    guardarBtns.forEach(btn => btn.classList.toggle('d-none', !modoEdicion));

    boton.innerHTML = modoEdicion
      ? '<i class="bi bi-eye"></i> Salir de edición'
      : '<i class="bi bi-pencil"></i> Activar edición';

    // Si se desactiva el modo edición, guardar todos los cambios
    if (!modoEdicion) {
      const dispositivosData = [];

      document.querySelectorAll('tr[data-id]').forEach(tr => {
        const id = tr.dataset.id;
        const data = { id };

        // Campos de la fila principal
        tr.querySelectorAll('input, select').forEach(input => {
          data[input.name] = input.value;
        });

        // Campos del bloque de detalle
        const detalle = document.getElementById(`detalle-${id}`);
        if (detalle) {
          detalle.querySelectorAll('input').forEach(input => {
            data[input.name] = input.value;
          });
        }

        dispositivosData.push(data);
      });

      fetch("/dispositivos/actualizar-multiple", {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dispositivosData)
      })
      .then(res => res.json())
      .then(response => {
        if (!response.success) {
          alert("Error al guardar los cambios");
        }
      });
    }
  });

  document.querySelectorAll('.toggle-detalle').forEach(btn => {
    btn.addEventListener('click', () => {
      const tr = btn.closest('tr');
      const id = tr.dataset.id;
      const detalle = document.getElementById(`detalle-${id}`);
      const icon = btn.querySelector('i');

      if (detalle.classList.contains('d-none')) {
        detalle.classList.remove('d-none');
        icon.classList.remove('bi-chevron-down');
        icon.classList.add('bi-chevron-up');
      } else {
        detalle.classList.add('d-none');
        icon.classList.remove('bi-chevron-up');
        icon.classList.add('bi-chevron-down');
      }
    });
  });
});