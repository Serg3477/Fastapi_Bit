function openLoginModal() {
  const container = document.getElementById('loginModalContainer');
  container.innerHTML = `
    <div class="modal-overlay active" data-modal="login">
      <div class="modal-box">
        <button class="modal-close" onclick="closeModal(this)">×</button>
        <form action="/login" method="post" class="form-contact">
          <h3 class="title">🔑 Login</h3>
          <table class="form-table">
            <tr>
              <td><label for="name">Name:</label></td>
              <td><input type="text" id="name" name="name" class="form-control" required></td>
            </tr>
            <tr>
              <td><label for="psw">Password:</label></td>
              <td><input type="password" id="psw" name="psw" class="form-control" required></td>
            </tr>
            <tr>
              <td><label for="remember">Remember me:</label></td>
              <td><input type="checkbox" id="remember" name="remember"></td>
            </tr>
          </table>
          <button type="submit" class="btn-create">Submit</button>
          <hr align="left" width="300px">
          <p><a href="#" onclick="openRegisterModal()">Registration</a></p>
        </form>
      </div>
    </div>
  `;
  if (window.location.pathname === "/login") {
      document.addEventListener("DOMContentLoaded", () => {
          openLoginModal();
      });
  }
}
