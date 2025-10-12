function openHistoryModal() {
  const container = document.getElementById('historyModalContainer');
  container.innerHTML = `
    <div class="modal-overlay active no-overlay" data-modal="history">
      <div class="modal-box history-box" id="historyBox">
        <button class="modal-close" onclick="closeModal(this)">×</button>
        <h3 class="title">📜 History Log</h3>
        <div class="history-content scrollable">
          <p>Loading history...</p>
        </div>
      </div>
    </div>
  `;

  // Make draggable
  makeDraggable(document.getElementById('historyBox'));

  // Fetch history
  fetch('/history')
    .then(res => res.json())
    .then(data => {
      const content = container.querySelector('.history-content');
      content.innerHTML = data.length === 0
        ? "<p>No history found.</p>"
        : data.map(entry => `
            <div class="history-entry">
              <strong>${entry.timestamp}</strong> — ${entry.action}: ${entry.details}
            </div>
          `).join('');
    });
}

// Drag logic
function makeDraggable(el) {
  let isDragging = false, offsetX = 0, offsetY = 0;

  el.addEventListener('mousedown', (e) => {
    isDragging = true;
    offsetX = e.clientX - el.offsetLeft;
    offsetY = e.clientY - el.offsetTop;
    el.style.position = 'absolute';
    el.style.zIndex = 1000;
  });

  document.addEventListener('mousemove', (e) => {
    if (isDragging) {
      el.style.left = `${e.clientX - offsetX}px`;
      el.style.top = `${e.clientY - offsetY}px`;
    }
  });

  document.addEventListener('mouseup', () => {
    isDragging = false;
  });
}
