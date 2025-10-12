function openUpdateUserModal(user) {
  const container = document.getElementById('updateUserModalContainer');
  container.innerHTML = `
    <div class="modal-overlay active" data-modal="update">
      <div class="modal-box">
        <button class="modal-close" onclick="closeModal(this)">×</button>
        <form id="updateUserForm" enctype="multipart/form-data" class="form-contact">
          <h3 class="title">🛠️ Update Profile</h3>
          <table class="form-table">
            <tr>
              <td><label for="name">Name:</label></td>
              <td><input type="text" id="name" name="name" class="form-control" value="${user.name}" required></td>
            </tr>
            <tr>
              <td><label for="email">Email:</label></td>
              <td><input type="email" id="email" name="email" class="form-control" value="${user.email}" required></td>
            </tr>
            <tr>
              <td><label for="psw">New Password:</label></td>
              <td><input type="password" id="psw" name="psw" class="form-control" placeholder="Leave blank to keep current"></td>
            </tr>
            <tr>
              <td><label for="avatar">New Avatar:</label></td>
              <td>
                <input type="file" id="avatar" name="avatar" accept=".jpg,.jpeg,.png">
                <img id="avatarPreview" class="avatar-preview" style="margin-top:10px; max-height:100px;">
              </td>
            </tr>
          </table>
          <button type="submit" class="btn-create">Update</button>
        </form>
      </div>
    </div>
  `;

  // Live preview for avatar
  const avatarInput = container.querySelector('#avatar');
  const avatarPreview = container.querySelector('#avatarPreview');
  avatarInput.addEventListener('change', () => {
    const file = avatarInput.files[0];
    if (file) {
      avatarPreview.src = URL.createObjectURL(file);
    } else {
      avatarPreview.src = "";
    }
  });

  // Submit handler
  const form = container.querySelector('#updateUserForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);

    try {
      const response = await fetch('/update_user', {
        method: 'POST',
        body: formData
      });

      if (response.redirected) {
        window.location.href = response.url;
      } else {
        showFlashMessage("❌ Error updating profile", "error");
      }
    } catch (err) {
      console.error("Update error:", err);
      showFlashMessage("❌ Server error", "error");
    }
  });
}

function showFlashMessage(message, category) {
  const flash = document.createElement('div');
  flash.className = `flash-message ${category}`;
  flash.textContent = message;
  document.body.appendChild(flash);
  setTimeout(() => flash.remove(), 4000);
}
