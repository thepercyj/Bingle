window.addEventListener('DOMContentLoaded', () => {
    let username = document.querySelector('.header').getAttribute('data-username');
    const usernameColor = getUsernameColor(username);

    // Create the container for the welcome message
    const welcomeMessage = document.createElement('span');
    welcomeMessage.textContent = 'Hello ';
    welcomeMessage.style.color = 'black'; // Set welcome message color

    // Create the container for the username
    const usernameElement = document.createElement('span');
    usernameElement.textContent = username;
    usernameElement.style.fontWeight = 'bold';
    usernameElement.style.color = usernameColor; // Set username color

    // Append both the welcome message and the username to the header
    const headerDiv = document.querySelector('.header');
    if (headerDiv) {
        headerDiv.appendChild(welcomeMessage); // Append "Welcome" part
        headerDiv.appendChild(usernameElement); // Append username part
    }

    function submit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);

        const endpointUrl = "/create-message/"
        fetch(endpointUrl, {
                method: "post",
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                },
            })
            .then(response => {
                this.state = response.ok ? 'success' : 'error';
                document.querySelector('textarea[name="content"]').value = ''; // Clears the textbox
                return response.json();
            })
            .then(data => {
                this.errors = data.errors || {};
            });
    }
    

});

let eventSource;
const sseData = document.getElementById('sse-data');

const colors = ['#D32F2F', '#C2185B', '#7B1FA2', '#512DA8', '#303F9F', '#1976D2', '#0288D1',
    '#0097A7', '#00796B', '#388E3C', '#689F38', '#AFB42B', '#FBC02D', '#FFA000', '#F57C00', '#E64A19',
    '#5D4037', '#616161', '#455A64'
];


function startSSE() {
    eventSource = new EventSource('/stream-chat-messages/');
    eventSource.onmessage = event => {
        const data = JSON.parse(event.data);
        console.log(data)
        const color = getUsernameColor(data.author__name);
        const formattedTime = formatTime(data.created_at); // You might need to implement formatTime
        const messageHTML = `
                <div class="message-box">
                    <br>
                    // <span class="message-time">Sent: ${formattedTime}</span>
                    <div class="message-author" style="color: ${color};"> <strong> ${data.author__name} </strong> </div>
                    <div class="chat-bubble chat-bubble--left">${data.content}</div>
                </div>`;
        sseData.innerHTML += messageHTML;
    };
}

function getUsernameColor(username) {
    // Simple hash function to index into the array of colors
    let hash = 0;
    for (let i = 0; i < username.length; i++) {
        hash = username.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash; // Convert to 32bit integer
    }
    hash = Math.abs(hash);
    return colors[hash % colors.length];
}

function formatTime(timeString) {
    const date = new Date(timeString)

    // Formats date as MM/DD/YY HH:MM
    const formattedDate = date.toLocaleDateString('en-GB');
    const formattedTime = date.toLocaleTimeString('en-GB', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    });
    return `${formattedDate} ${formattedTime}`;
}


// On load, start SSE if the browser supports it.
if (typeof (EventSource) !== 'undefined') {
    startSSE();
} else {
    sseData.innerHTML = 'Whoops! Your browser doesn\'t receive server-sent events.';
}


$(function () {
    $(".friend-drawer--onhover").on("click", function () {
        $(".chat-bubble").hide("slow").show("slow");
    });
});