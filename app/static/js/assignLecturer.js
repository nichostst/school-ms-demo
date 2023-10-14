const form = document.getElementById('assign_lecturers');

function assignLecturers(e) {
    e.preventDefault();
    let all_dropdowns = Array.from(document.querySelectorAll('[id^="dropdown-"]'));
    let id_value = all_dropdowns.map(
        elements => [elements.id, Array.from(elements.selectedOptions).map(o => o.value)]
    );

    fetch("/api/coordinator/assign_lecturer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
            id_value: id_value
        }),
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        form.reset();
        info = document.getElementById('create_status_info');

        if (data.result === 'success') {
            message = 'Assignment successful!';
        } else if (data.result === 'partial') {
            message = 'Assignment partially successful!';
        } else if (data.result === 'failure') {
            message = 'Assignment failed!';
            info.style = 'color: rgb(200, 0, 0); background-color: rgba(200, 90, 90, 0.3);'
        };
        info.innerText = message;
        info.style.visibility = "visible"
    })
    .catch((err) => {
        console.log(err);
    });
};

form.addEventListener('submit', assignLecturers);