$(document).ready(function() {
    const editPlayerModal = document.getElementById('editPlayerModal');
    
    if (editPlayerModal) {
        editPlayerModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const jugadorId = button.dataset.jugadorId;
            const dorsal = button.dataset.dorsal;
            const altura = button.dataset.altura;
            const peso = button.dataset.peso;
            const piernaHabil = button.dataset.piernaHabil;
            const posicion = button.dataset.posicion;
            const esCapitan = button.dataset.esCapitan === 'True';
            const jugadorNombre = button.dataset.jugadorNombre;
            
            console.log('PESO desde button.dataset:', peso, 'tipo:', typeof peso);
            
            // Llenar el modal con los datos
            document.getElementById('jugadorIdInput').value = jugadorId;
            document.getElementById('dorsalInput').value = dorsal === '0' ? '' : dorsal;
            document.getElementById('alturaInput').value = altura || '';
            document.getElementById('pesoInput').value = peso ? parseFloat(peso) : '';
            document.getElementById('piernaHabilInput').value = piernaHabil || '';
            document.getElementById('posicionInput').value = posicion || '';
            document.getElementById('esCapitanInput').checked = esCapitan;
            
            console.log('PESO asignado al input:', document.getElementById('pesoInput').value);
            
            // Actualizar el título con el nombre del jugador
            document.getElementById('editPlayerLabel').textContent = `✏️ Editar: ${jugadorNombre}`;
        });
    }
    
    // Manejar el envío del formulario
    const formularioEditar = document.getElementById('formulario_editar_jugador');
    if (formularioEditar) {
        formularioEditar.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const jugadorId = document.getElementById('jugadorIdInput').value;
            const formData = new FormData(this);
            
            // Construir la URL
            const url = apiUrlEditarJugador.replace('{jugador_id}', jugadorId);
            
            // Mostrar loading
            const submitBtn = formularioEditar.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Guardando...';
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showAlert('success', '✓ Información del jugador actualizada');
                    
                    // Cerrar modal
                    setTimeout(() => {
                        bootstrap.Modal.getInstance(editPlayerModal).hide();
                        // Recargar la página para ver los cambios
                        location.reload();
                    }, 1500);
                } else {
                    showAlert('danger', `✗ Error: ${data.error}`);
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="bi bi-check-lg"></i> Guardar cambios';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', '✗ Error al guardar los cambios');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="bi bi-check-lg"></i> Guardar cambios';
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