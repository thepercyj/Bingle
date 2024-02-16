// JavaScript functions to open and close the modal
function openModal() {
    document.getElementById('myModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    var modal = document.getElementById('myModal');
    if (event.target === modal) {
        closeModal();
    }
};