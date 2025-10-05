function openUpdateModal(button) {
  const container = document.getElementById('updateModalContainer');
  const id = button.dataset.id;
  const token = button.dataset.token;
  const quantity = button.dataset.quantity;
  const price = button.dataset.price;

  container.innerHTML = `
    <div class="modal-overlay active" data-modal="update">
      <div class="modal-box">
        <button class="modal-close" onclick="closeModal(this)">×</button>
        <form action="/update/${id}" method="post" class="form-contact">
          <h3 class="title">📝 Update record - ${token}</h3>
          <table class="form-table">
            <tr>
              <td><label for="token">Token:</label></td>
              <td><input type="text" id="token" name="token" value="${token}" class="form-control"></td>
            </tr>
            <tr>
              <td><label for="quantity">Quantity:</label></td>
              <td><input type="number" id="quantity" name="quantity" value="${quantity}" step="0.001" class="form-control"></td>
            </tr>
            <tr>
              <td><label for="price">Price:</label></td>
              <td><input type="number" id="price" name="price" value="${price}" step="0.001" class="form-control"></td>
            </tr>
          </table>
          <button type="submit" class="btn-create">Success</button>
        </form>
      </div>
    </div>
  `;
}


