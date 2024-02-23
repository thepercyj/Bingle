// JavaScript function to open a specified modal by ID
function openModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

// JavaScript function to close a specified modal by ID
function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    // Check if the clicked element is a modal
    if (event.target.classList.contains('modal')) {
        // Use the style display property to close it
        event.target.style.display = 'none';
    }
};
