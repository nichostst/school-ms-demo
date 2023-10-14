const form = document.getElementById('grade_restructure_form');

function gradeRestructure(e) {
    e.preventDefault();
    let structure_inputs = Array.from(document.querySelectorAll('.structure_input'));
    let new_structures = structure_inputs.map(
        element => ({
            "structure_id": element.name,
            "structure_weight": element.value
        })
    );
    console.log(new_structures);

    fetch("/api/coordinator/grade_restructure", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
            new_structures: new_structures
        }),
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        form.reset();
        info = document.getElementById('create_status_info');

        if (data.result === 'success') {
            window.location.replace(data.redirect_to);
        } else if (data.result === 'weight_failure') {
            message = 'Weights do not sum up to 100%, please check your input.';
            info.style = 'color: rgb(200, 0, 0); background-color: rgba(200, 90, 90, 0.3);'
        } else if (data.result === 'min_weight_failure') {
            message = 'Minimum weight for a structure is 5%, please check your input.';
            info.style = 'color: rgb(200, 0, 0); background-color: rgba(200, 90, 90, 0.3);'
        };

        info.innerText = message;
        info.style.visibility = "visible"
    })
    .catch((err) => {
        console.log(err);
    });
};

form.addEventListener('submit', gradeRestructure);