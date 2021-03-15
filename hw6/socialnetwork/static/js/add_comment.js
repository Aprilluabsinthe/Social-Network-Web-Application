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

function getFollower() {
    let request = new XMLHttpRequest()
    request.onreadystatechange = function () {
        if (request.readyState != 4) return
        updatePage(request)
    }

    request.open("GET", "/socialnetwork/get-follower", true)
    request.send()
}

function updatePage(request) {
    if (request.status != 200 && request.status != 404 ) {
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

function updateGlobal(posts) {
    // Removes the old to-do list items
    let list = document.getElementById("postshow")
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
            deleteButton = "<button onclick='deletePost(" + post.post_id + ")'>Delete</button> "
        } else {
            deleteButton = "<button style='visibility: hidden'>Delete</button> "
        }

        let element = document.createElement("div")
        element.innerHTML =
            deleteButton + '<p class="lead">' +
            '<a href="profile/' + post.user+ '">' +
            '<span class="message" id="id_post_profile_' + post.id + '">' +
            post.first_name + " " + post.last_name +
            '</span></a></p>' +
            '<p align="center">' +
            '<span class="lead" id="id_post_text_' + post.post_id + '">' +
            post.content +
            '</span></p>' +
            '<p align="right" class="small dark-teal-text h-50">' +
            '<span id="id_post_date_time_' + post.id+ '">' +
            post.time +
            '</span></p></span>' +
            "        <div>" +
            '            <div class="col dark-teal-text">' +
            "                comment" +
            "            </div>" +
            "            <div>" +
            '                <input id = "id_comment_input_text_' + post.post_id + '" name="comment" class="form-control" type="text">' +
            "            </div>" +
            '            <div align="right">' +
            '                <button id="id_comment_button_' + post.post_id+ '" onclick="addComment("' + post.post_id + '")" >Submit</button>' +
            "            </div>" +
            "        </div>" +
            "    <hr>"
        // Adds the todo-list item to the HTML list
        list.appendChild(element)
    }
}

function updateComment(){

    // Removes the old to-do list items
    let list = document.getElementById("commentshow")
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
            deleteButton = "<button onclick='deletePost(" + post.post_id + ")'>Delete</button> "
        } else {
            deleteButton = "<button style='visibility: hidden'>Delete</button> "
        }

        let element = document.createElement("div")
        element.innerHTML =
            deleteButton
        // Adds the todo-list item to the HTML list
        list.appendChild(element)
    }
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

function addComment(postid){
    let elementId = "id_comment_input_text_" + postid;
    let commentTextElement = document.getElementById(elementId)
    let commentTextValue = commentTextElement.value

    // Clear input box and old error message (if any)
    commentTextElement.value = "";
    displayError("");

    let request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState != 4) return
        updatePage(request)
    }

    request.open("POST", "/socialnetwork/makecomment" + postid, true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send("content="+postTextValue+"parentid="+postid+"&csrfmiddlewaretoken="+getCSRFToken());
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

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
}



