// JavaScript function to open a specified modal by ID
function openViewModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
    //populateTable();
}

function openBookModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

function openLibraryModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

function openUploadModal(modalId) {
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


$(document).ready(function(){
    // Function to close modal
    function closeModal(modalId) {
        $('#' + modalId).css('display', 'none');
    }

    // Handle click on upload button
    $('#upload-btn').click(function(){
        var formData = new FormData($('#upload-form')[0]);
        $.ajax({
            url: '/img_upload/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response){
                if(response.success){
                    // Redirect or do something on success
                    window.location.href = "";
                } else {
                    // Show error message in modal
                    $('#error-message').text(response.error);
                    $('#picture-modal').css('display', 'flex');
                }
            },
            error: function(xhr, status, error){
                console.error(xhr.responseText);
                // Handle other errors if needed
            }
        });
    });

    // Close modal when clicking on the close button
    $('.close-btn').click(function(){
        closeModal('picture-modal');
    });

    // Close modal when clicking outside of it
    $(window).click(function(event){
        if(event.target == $('#picture-modal')[0]){
            closeModal('picture-modal');
        }
    });
});

// Function to show search results
function showSearchResults() {
    document.getElementById('search-results').style.display = 'block';
}

// Function to hide search results
function hideSearchResults() {
    document.getElementById('search-results').style.display = 'none';
}

// Event listener for form submission
document.getElementById('search-form').addEventListener('submit', function(event) {
    // Show search results when the form is submitted
    showSearchResults();
});


function hideTable() {
    document.getElementById('user-profile-table').style.display = 'none';
}

