function openCreateModal() {
  const container = document.getElementById('createModalContainer');
  container.innerHTML = `
    <div class="modal-overlay active" data-modal="create">
      <div class="modal-box">
        <button class="modal-close" onclick="closeModal(this)">×</button>
        <form action="/create" method="post" class="form-contact">
          <h3 class="title">➕ Create new record</h3>
          <table class="form-table">
            <tr>
              <td><label for="token">Token:</label></td>
              <td><input type="text" id="token" name="token" class="form-control"></td>
            </tr>
            <tr>
              <td><label for="quantity">Quantity:</label></td>
              <td><input type="number" id="quantity" name="quantity" step="0.001" class="form-control"></td>
            </tr>
            <tr>
              <td><label for="price">Price:</label></td>
              <td><input type="number" id="price" name="price" step="0.001" class="form-control"></td>
            </tr>
          </table>
          <button type="submit" class="btn-create">Create</button>
        </form>
      </div>
    </div>
  `;
}

