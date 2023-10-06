const register_form = document.getElementById('login_form');

function login(e) {
    e.preventDefault();
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({ email: email, password: password }),
    })
    .then((res) => res.json())
    .then((data) => {
        console.log(data);
        if (data.success) {
            window.location.href = "/home";
        }
    })
    .catch((err) => {
        console.log(err);
    });
};

register_form.addEventListener('submit', login);