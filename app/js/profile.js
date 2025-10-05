function openProfileModal() {
  const user = window.currentUser || {};
  const name = user.name || "—";
  const email = user.email || "—";
  const avatar = user.avatar || "/static/Images/default.png";

  const container = document.getElementById('profileModalContainer');
  container.innerHTML = `
    <div class="modal-overlay active" data-modal="profile">
      <div class="modal-box profile-box">
        <button class="modal-close" onclick="closeModal(this)">×</button>
        <div class="profile-card">
          <img src="/${avatar || 'static/Images/avatar.png'}" 
               alt="Avatar" class="profile-avatar">
          <h3 class="profile-title">User Profile</h3>
          <ul class="profile-list">
            <li><strong>Name:</strong>${name || ''}</li>
            <li><strong>Email:</strong>${email || ''}</li>
          </ul>
          <div class="profile-actions">
            <a href="#" class="btn-update">Update</a>
            <a href="/delete_user" class="btn-delete">Delete</a>
            <a href="/logout" class="btn-logout">Logout</a>
          </div>
        </div>
      </div>
    </div>
  `;
}
