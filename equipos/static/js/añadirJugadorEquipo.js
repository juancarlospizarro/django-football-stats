document.addEventListener('DOMContentLoaded', function() {
    const addPlayerBtns = document.querySelectorAll('.add-player-btn');

    addPlayerBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const equipoId = this.dataset.equipoId;
            const jugadorId = this.dataset.jugadorId;
            const jugadorNombre = this.dataset.jugadorNombre;
            const btn = this;

            // Mostrar loading
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Añadiendo jugador...';

            // Construir la URL usando la variable global
            const url = apiUrlAgregarJugador
                .replace('{equipo_id}', equipoId)
                .replace('{jugador_id}', jugadorId);

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('success', `✓ ${jugadorNombre} añadido al equipo`);
                    
                    btn.closest('.list-group-item').remove();
                    
                    const listGroup = document.querySelector('.list-group');
                    if (!listGroup || listGroup.children.length === 0) {
                        const modal = document.querySelector('#addPlayerModal .modal-body');
                        modal.innerHTML = '<div class="alert alert-info"><i class="bi bi-info-circle"></i> No hay jugadores disponibles sin equipo.</div>';
                    }
                    
                    setTimeout(() => {
                        bootstrap.Modal.getInstance(document.getElementById('addPlayerModal')).hide();
                        // Recargar la página para ver los cambios
                        location.reload();
                    }, 2000);
                } else {
                    showAlert('danger', `✗ Error: ${data.error}`);
                    btn.disabled = false;
                    btn.innerHTML = '<i class="bi bi-plus-lg"></i> Añadir';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', '✗ Error al añadir jugador');
                btn.disabled = false;
                btn.innerHTML = '<i class="bi bi-plus-lg"></i> Añadir';
            });
        });
    });
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