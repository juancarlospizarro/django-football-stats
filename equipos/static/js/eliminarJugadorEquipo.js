$(document).ready(function() {
    const confirmRemovePlayerModal = document.getElementById('confirmRemovePlayerModal');
    
    if (confirmRemovePlayerModal) {
        confirmRemovePlayerModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const equipoId = button.dataset.equipoId;
            const jugadorId = button.dataset.jugadorId;
            const jugadorNombre = button.dataset.jugadorNombre;
            
            // Actualizar el título del modal
            document.getElementById('confirmRemovePlayerLabel').textContent = `¿Eliminar a ${jugadorNombre}?`;
            
            // Guardar los datos en el botón de confirmación
            const confirmBtn = document.getElementById('confirmRemovePlayerBtn');
            confirmBtn.dataset.equipoId = equipoId;
            confirmBtn.dataset.jugadorId = jugadorId;
            confirmBtn.dataset.jugadorNombre = jugadorNombre;
        });
    }
    
    // Manejar el clic en el botón de confirmación
    const confirmRemoveBtn = document.getElementById('confirmRemovePlayerBtn');
    if (confirmRemoveBtn) {
        confirmRemoveBtn.addEventListener('click', function() {
            const equipoId = this.dataset.equipoId;
            const jugadorId = this.dataset.jugadorId;
            const jugadorNombre = this.dataset.jugadorNombre;
            
            // Mostrar loading
            this.disabled = true;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Eliminando...';
            
            // Construir la URL
            const url = apiUrlEliminarJugador.replace('{equipo_id}', equipoId).replace('{jugador_id}', jugadorId);
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('success', `✓ ${jugadorNombre} eliminado del equipo`);
                    
                    // Cerrar modal
                    setTimeout(() => {
                        bootstrap.Modal.getInstance(confirmRemovePlayerModal).hide();
                        // Recargar la página para ver los cambios
                        location.reload();
                    }, 1500);
                } else {
                    showAlert('danger', `✗ Error: ${data.error}`);
                    confirmRemoveBtn.disabled = false;
                    confirmRemoveBtn.innerHTML = '<i class="bi bi-trash-fill"></i> Sí, eliminar jugador';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', '✗ Error al eliminar el jugador');
                confirmRemoveBtn.disabled = false;
                confirmRemoveBtn.innerHTML = '<i class="bi bi-trash-fill"></i> Sí, eliminar jugador';
            });
        });
    }
});

// Función para mostrar alertas
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, 4000);
}
