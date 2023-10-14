const form = document.getElementById('structure_creation_form');

function gradeRestructure(e) {
    e.preventDefault();
    let structure_inputs = Array.from(document.querySelectorAll('.structure_name'));
    let weight_inputs = Array.from(document.querySelectorAll('.weightage'));
    let structures = structure_inputs.map(
        element => element.value
    );
    let weights = weight_inputs.map(
        element => element.value
    );

    fetch("/api/coordinator/add_structure", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
            structures: structures,
            weights: weights
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