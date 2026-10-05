// ========================================
// STUDENT PERFORMANCE SYSTEM
// Main JavaScript
// ========================================


// ========================================
// DELETE CONFIRMATION
// ========================================

function confirmDelete(itemName) {

    return confirm(
        "Are you sure you want to delete " +
        itemName +
        "?"
    );
}


// ========================================
// AUTO HIDE ALERTS
// ========================================

document.addEventListener("DOMContentLoaded", function () {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        // Only automatically hide success messages
        if (alert.classList.contains("alert-success")) {

            setTimeout(function () {

                alert.style.transition = "opacity 0.5s";

                alert.style.opacity = "0";

                setTimeout(function () {
                    alert.remove();
                }, 500);

            }, 4000);
        }

    });

});


// ========================================
// SCORE VALIDATION
// ========================================

function validateScore(input) {

    const score = parseFloat(input.value);

    if (isNaN(score)) {
        return true;
    }

    if (score < 0 || score > 100) {

        alert(
            "Score must be between 0 and 100."
        );

        input.value = "";

        return false;
    }

    return true;
}


// ========================================
// ADD SCORE VALIDATION TO FORMS
// ========================================

document.addEventListener("DOMContentLoaded", function () {

    const scoreInputs =
        document.querySelectorAll(
            'input[name="score"]'
        );

    scoreInputs.forEach(function (input) {

        input.addEventListener(
            "change",
            function () {

                validateScore(input);

            }
        );

    });

});


// ========================================
// TABLE SEARCH
// ========================================

function searchTable(inputId, tableId) {

    const input =
        document.getElementById(inputId);

    const table =
        document.getElementById(tableId);

    if (!input || !table) {
        return;
    }

    input.addEventListener(
        "keyup",
        function () {

            const searchText =
                input.value.toLowerCase();

            const rows =
                table.querySelectorAll(
                    "tbody tr"
                );

            rows.forEach(function (row) {

                const text =
                    row.textContent.toLowerCase();

                if (text.includes(searchText)) {

                    row.style.display = "";

                } else {

                    row.style.display = "none";

                }

            });

        }
    );
}


// ========================================
// CONFIRM DELETE FOR FORMS
// ========================================

document.addEventListener("DOMContentLoaded", function () {

    const deleteForms =
        document.querySelectorAll(
            "form[data-confirm-delete]"
        );

    deleteForms.forEach(function (form) {

        form.addEventListener(
            "submit",
            function (event) {

                const message =
                    form.getAttribute(
                        "data-confirm-delete"
                    ) ||
                    "Are you sure you want to delete this record?";

                if (!confirm(message)) {

                    event.preventDefault();

                }

            }
        );

    });

});


// ========================================
// LOGIN TOKEN HELPER
// ========================================

function getAccessToken() {

    return localStorage.getItem(
        "access_token"
    );
}


// ========================================
// LOGOUT
// ========================================

function logout() {

    localStorage.removeItem(
        "access_token"
    );

    window.location.href = "/login";
}