function openRegisterModal() {
  const container = document.getElementById('registerModalContainer');
  container.innerHTML = `
    <div class="modal-overlay active" data-modal="register">
      <div class="modal-box">
        <button class="modal-close" onclick="closeModal(this)">×</button>
        <form action="/register" method="post" enctype="multipart/form-data" class="form-contact">
          <h3 class="title">🧾 Registration</h3>
          <table class="form-table">
            <tr>
              <td><label for="name">Name:</label></td>
              <td><input type="text" id="name" name="name" class="form-control" required></td>
            </tr>
            <tr>
              <td><label for="email">Email:</label></td>
              <td><input type="email" id="email" name="email" class="form-control" required></td>
            </tr>
            <tr>
              <td><label for="psw">Password:</label></td>
              <td><input type="password" id="psw" name="psw" class="form-control" required></td>
            </tr>
            <tr>
              <td><label for="avatar">Avatar (path):</label></td>
              <td><input type="file" id="avatar" name="avatar" accept=".jpg,.jpeg,.png"></td>
            </tr>
          </table>
          <button type="submit" class="btn-create">Register</button>
        </form>
      </div>
    </div>
  `;

  // При желании — автофокус:
  const nameInput = container.querySelector('#name');
  if (nameInput) nameInput.focus();
}
