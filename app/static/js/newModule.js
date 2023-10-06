const form = document.getElementById('admin_new_module');

function register(e) {
    e.preventDefault();
    let module_code = document.getElementById('module_code').value;
    let module_name = document.getElementById('module_name').value;
    let credits = document.getElementById('credits').value;

    fetch("/api/admin/new_module", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({ module_code: module_code, module_name: module_name, credits: credits }),
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        form.reset();
        message = 'Module ' + module_name + ' has been successfully created!';
        info = document.getElementById('create_status_info');
        info.innerText = message;
        info.style.visibility = "visible"
    })
    .catch((err) => {
        console.log(err);
    });
};

form.addEventListener('submit', register);