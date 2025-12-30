document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendario');
    if (!calendarEl) return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        firstDay: 1,
        height: 'auto'
    });

    calendar.render();
});
