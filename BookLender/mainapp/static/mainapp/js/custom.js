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

function populateTable() {
    fetch('/list-book/')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('book-table');
            // Clear existing table content
            tableBody.innerHTML = '';
            // Create table header row
            const headerRow = document.createElement('tr');
            headerRow.innerHTML = `
                <th>Title</th>
                <th>Author</th>
                <th>Genre</th>
                <th>Published Date</th>
            `;
            tableBody.appendChild(headerRow);
            // Populate table with fetched data
            data.forEach(book => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${book.book_title}</td>
                    <td>${book.book_author}</td>
                    <td>${book.genre}</td>
                    <td>${book.published_date}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}


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
const picture = urlParams.get('picture');
if (picture === 'true') {
 openUploadModal('picture-modal')
}
});
