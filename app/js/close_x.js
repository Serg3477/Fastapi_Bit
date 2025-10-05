function closeModal(button) {
  // ищем ближайший родитель с классом modal-overlay
  const modal = button.closest('.modal-overlay');
  if (modal) modal.remove();
}

// function closeModal(button) {
//   const overlay = button.closest('.modal-overlay');
//   if (!overlay) return;
//   overlay.classList.add('closing');
//   overlay.addEventListener('animationend', () => overlay.remove(), { once: true });
// }
