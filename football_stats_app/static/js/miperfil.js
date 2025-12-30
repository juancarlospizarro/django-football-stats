document.addEventListener("DOMContentLoaded", function () {
    const deleteBtn = document.getElementById("confirmDeleteBtn");

    deleteBtn.addEventListener("click", function () {
        const url = deleteBtn.dataset.url;

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const confirmModal = bootstrap.Modal.getInstance(
                    document.getElementById("confirmDeleteModal")
                );
                confirmModal.hide();

                const successModal = new bootstrap.Modal(
                    document.getElementById("deletedSuccessModal")
                );
                successModal.show();

                setTimeout(() => {
                    window.location.href = "/";
                }, 2000);
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
