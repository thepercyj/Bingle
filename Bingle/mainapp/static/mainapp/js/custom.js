// nav menu style
var nav = $("#navbarSupportedContent");
var btn = $(".custom_menu-btn");
btn.click
btn.click(function (e) {

e.preventDefault();
nav.toggleClass("lg_nav-toggle");
document.querySelector(".custom_menu-btn").classList.toggle("menu_btn-style")
});


function getCurrentYear() {
var d = new Date();
var currentYear = d.getFullYear()

$("#displayDate").html(currentYear);
}

getCurrentYear();


document.addEventListener("DOMContentLoaded", function() {
const urlParams = new URLSearchParams(window.location.search);
const addbook = urlParams.get('add-book');
if (addbook === 'true') {
openBookModal('add-book-modal')
}
});

document.addEventListener("DOMContentLoaded", function() {
const urlParams = new URLSearchParams(window.location.search);
const book = urlParams.get('book');
if (book === 'true') {
openViewModal('book-modal')
}
});

document.addEventListener("DOMContentLoaded", function() {
const urlParams = new URLSearchParams(window.location.search);
const borrow = urlParams.get('borrow');
if (borrow === 'true') {
openViewModal('borrow-modal')
}
});

document.addEventListener("DOMContentLoaded", function() {
const urlParams = new URLSearchParams(window.location.search);
const booking = urlParams.get('booking');
if (booking === 'true') {
openViewModal('booking-modal')
}
});

document.addEventListener("DOMContentLoaded", function() {
const urlParams = new URLSearchParams(window.location.search);
const picture = urlParams.get('picture');
if (picture === 'true') {
openUploadModal('picture-modal')
}
});

document.addEventListener("DOMContentLoaded", function() {
const urlParams = new URLSearchParams(window.location.search);
const library = urlParams.get('library');
if (library === 'true') {
openLibraryModal('library-modal')
}
});

$(document).ready(function() {
$(".notification-drop .item").on('click',function() {
$(this).find('ul').toggle();
});
});

function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Check if the cookie name matches the specified name
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}

function loadUserBooks(url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.querySelector('.user_books').innerHTML = data;
        });
}

function loadLibraryBooks(url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.querySelector('.library').innerHTML = data;
        });
}

document.addEventListener('DOMContentLoaded', () => {
    // Event listener for pagination links in My Library section
    document.querySelectorAll('.user-books-pagination').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.href;
            loadUserBooks(url);
        });
    });

    // Event listener for pagination links in Bingle Store section
    document.querySelectorAll('.library-pagination').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.href;
            loadLibraryBooks(url);
        });
    });

    // Add a check to ensure the 'reveal' element exists
    var revealElement = document.getElementById('reveal');
    if (revealElement) {
        revealElement.addEventListener('click', function() {
            // Add console.log statements to debug
            console.log('Reveal button clicked.');

            var selectedOwner = document.getElementById('owner').value;
            console.log('Selected owner:', selectedOwner);

            if (selectedOwner) {
                // Add a check to ensure the 'booking-form' element exists
                var bookingForm = document.getElementById('booking-form');
                if (bookingForm) {
                    // Display the 'booking-form'
                    bookingForm.style.display = 'block';
                    console.log('Booking form displayed.');
                } else {
                    console.error('Booking form element not found.');
                }
            } else {
                console.error('No owner selected.');
            }
        });
    } else {
        console.error('Reveal button element not found.');
    }
});


function searchUserBooks() {
    var query = document.getElementById("searchUserBooks").value;
    window.location.href = '/new_home/?user_books_search=' + query;
}

function searchLibrary() {
    var query = document.getElementById("searchLibrary").value;
    window.location.href = '/new_home/?library_search=' + query;
}

function libraryPress(event) {
    // Check if the key pressed is "Enter"
    if (event.key === 'Enter') {
        // Trigger the search function
        searchUserBooks();
    }
}

function storePress(event) {
    // Check if the key pressed is "Enter"
    if (event.key === 'Enter') {
        // Trigger the search function
        searchLibrary();
    }
}


//document.getElementById('reveal').addEventListener('click', function() {
//    var selectedOwner = document.getElementById('owner').value;
//    if (selectedOwner) {
//        document.getElementById('booking-form').style.display = 'block';
//    }
//});
