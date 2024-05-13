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

//function populateTable() {
//    fetch('/list-book/')
//        .then(response => response.json())
//        .then(data => {
//            const tableBody = document.getElementById('book-table');
//            // Clear existing table content
//            tableBody.innerHTML = '';
//            // Create table header row
//            const headerRow = document.createElement('tr');
//            headerRow.innerHTML = `
//                <th>Title</th>
//                <th>Author</th>
//                <th>Genre</th>
//                <th>Published Date</th>
//            `;
//            tableBody.appendChild(headerRow);
//            // Populate table with fetched data
//            data.forEach(book => {
//                const row = document.createElement('tr');
//                row.innerHTML = `
//                    <td>${book.book_title}</td>
//                    <td>${book.book_author}</td>
//                    <td>${book.genre}</td>
//                    <td>${book.published_date}</td>
//                `;
//                tableBody.appendChild(row);
//            });
//        })
//        .catch(error => console.error('Error fetching data:', error));
//}


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

// document.addEventListener("DOMContentLoaded", function() {
// // Get all sub-menu items
// var subMenuItems = document.querySelectorAll(".notification-drop .sub-menu li");
//
// // Add event listener to each sub-menu item
// subMenuItems.forEach(function(item) {
//     item.addEventListener("click", function() {
//         callDecrementNotificationCounterFunction();
//     });
// });
//
// function callDecrementNotificationCounterFunction() {
//     // Send an AJAX request to call the decrement_notification_counter function
//     var xhr = new XMLHttpRequest();
//     var csrftoken = getCookie('csrftoken');
//     xhr.open("POST", "/decrement_counter/", true);
//     xhr.setRequestHeader("X-CSRFToken", csrftoken);
//     xhr.setRequestHeader("Content-Type", "application/json");
//     xhr.onreadystatechange = function() {
//         if (xhr.readyState === 4 && xhr.status === 200) {
//             // Handle response if needed
//             // For example, you can update the UI here if necessary
//         }
//     };
//     xhr.send();
// }
// });

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
});


function searchUserBooks() {
    var query = document.getElementById("searchUserBooks").value;
    window.location.href = '/profile_page/?user_books_search=' + query;
}

function searchStore() {
    var query = document.getElementById("searchStore").value;
    window.location.href = '/profile_page/?store_search=' + query;
}

function searchLibrary() {
    var query = document.getElementById("searchLibrary").value;
    window.location.href = '/profile_page/?library_search=' + query;
}


document.getElementById('reveal-form').addEventListener('click', function() {
    var selectedOwner = document.getElementById('owner').value;
    if (selectedOwner) {
        document.getElementById('booking-form').style.display = 'block';
    }
});
