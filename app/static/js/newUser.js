const form = document.getElementById('admin_new_user');

function register(e) {
    e.preventDefault();
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    let role = document.getElementById('user-type').value;

    fetch("/api/admin/new_user", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({ username: username, email: email, password: password, role: role }),
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        form.reset();
    })
    .catch((err) => {
        console.log(err);
    });
};

form.addEventListener('submit', register);