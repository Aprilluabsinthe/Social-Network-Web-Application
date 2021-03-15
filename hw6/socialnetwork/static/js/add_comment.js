"use strict"

function getGlobal() {
    let request = new XMLHttpRequest()
    request.onreadystatechange = function () {
        if (request.readyState != 4) return
        updatePage(request)
    }

    request.open("GET", "/socialnetwork/get-global", true)
    request.send()
}

function updatePage(request) {
    if (request.status != 200) {
        displayError("Received status code = " + request.status)
        return
    }

    let response = JSON.parse(request.responseText)
    if (Array.isArray(response)) {
        updateGlobal(response)
    } else if (response.hasOwnProperty('error')) {
        displayError(response.error)
    } else {
        displayError(response)
    }
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}

function addPost(){
    let postTextElement = document.getElementById("id_post_input_text")
    let postTextValue = postTextElement.value

    // Clear input box and old error message (if any)
    postTextElement.value = "";
    displayError("");

    let request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState != 4) return
        updatePage(request)
    }

    request.open("POST", "/socialnetwork/makepost", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send("post="+postTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}

// action="{% url 'delete-post' post.id %}"
function deletePost(id) {
    let request = new XMLHttpRequest()
    request.onreadystatechange = function () {
        if (request.readyState != 4) return
        updatePage(request)
    }

    request.open("POST", "/socialnetwork/delete-post/" + id, true)
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    request.send("csrfmiddlewaretoken=" + getCSRFToken())
}

// function sanitize(s) {
//     // Be sure to replace ampersand first
//     if(s!=null){
//         return s.replace(/&/g, '&amp;')
//             .replace(/</g, '&lt;')
//             .replace(/>/g, '&gt;')
//             .replace(/"/g, '&quot;')
//     }
//     return s
// }

function updateGlobal(posts) {
    // Removes the old to-do list items
    let list = document.getElementById("posts")
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild)
    }

    // Adds each new post item to the list
    for (let i = 0; i < posts.length; i++) {
        let post = posts[i]

        // Builds a new HTML list item for the post
        let deleteButton
        if (post.user === myUserName) {
            // action="{% url 'delete-post' post.id %}"
            deleteButton = "<button onclick='deletePost(" + post.id + ")'>Delete</button> "
        } else {
            deleteButton = "<button style='visibility: hidden'>Delete</button> "
        }

        let element = document.createElement("div")
        element.innerHTML =
            deleteButton +
            '<span className="col-lg">Published by' +
            '<p className="lead">' +
            '<a href="{% url \'profile\' post.user.id %}">' +
            '<span className="message"' +
            'id="id_post_profile_{{post.id}}">' +
            post.user.username +
            '</span></a></p>' +
            '<p align="center">' +
            '<span className="lead" id="id_post_text_{{post.id}}">' +
            post.content +
            '</span></p>' +
            '<p align="right" className="small dark-teal-text h-50">' +
            '<span id="id_post_date_time_{{post.id}}">' +
            post.time +
            '</span></p></span>'

        // Adds the todo-list item to the HTML list
        list.appendChild(element)
    }
}

