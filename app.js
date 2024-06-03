document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(loginForm);
            const data = {
                username: formData.get('username'),
                password: formData.get('password')
            };
            try {
                const response = await axios.post('/login', data);
                if (response.data.success) {
                    window.location.href = '/admin';
                } else {
                    alert(response.data.message);
                }
            } catch (error) {
                console.error(error);
            }
        });
    }

    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(registerForm);
            const data = {
                username: formData.get('username'),
                password: formData.get('password')
            };
            try {
                const response = await axios.post('/register', data);
                if (response.data.success) {
                    window.location.href = '/login';
                } else {
                    alert(response.data.message);
                }
            } catch (error) {
                console.error(error);
            }
        });
    }
});

async function logout() {
    try {
        await axios.get('/logout');
        window.location.href = '/';
    } catch (error) {
        console.error(error);
    }
}

async function editUser(id, username) {
    const newUsername = prompt("Novo nome de usuário:", username);
    if (newUsername) {
        try {
            const response = await axios.put(`/admin/users/${id}`, { username: newUsername });
            if (response.data.success) {
                location.reload();
            } else {
                alert(response.data.message);
            }
        } catch (error) {
            console.error(error);
        }
    }
}

async function deleteUser(id) {
    if (confirm("Tem certeza que deseja excluir este usuário?")) {
        try {
            const response = await axios.delete(`/admin/users/${id}`);
            if (response.data.success) {
                location.reload();
            } else {
                alert(response.data.message);
            }
        } catch (error) {
            console.error(error);
        }
    }
}
