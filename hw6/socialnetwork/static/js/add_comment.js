"use strict"
function showPost(){

}

function getGlobal() {
    $.ajax({
        url: "/socialnetwork/get-global",
        dataType : "json",
        success: updatePage,
        error: updateError
    });
}

function getFollower() {
    $.ajax({
        url: "/socialnetwork/get-follower",
        dataType : "json",
        success: updatePage,
        error: updateError
    });
}

function getComment() {
    $.ajax({
        url: "/socialnetwork/get-comment",
        dataType : "json",
        success: updatePage,
        error: updateError
    });
}

function updatePage(response) {
    if (Array.isArray(response)) {
        updateGlobal(response)
    } else if (response.hasOwnProperty('error')) {
        displayError(response.error)
    } else {
        displayError(response)
    }
}


function dictToURI(dict) {
  var str = [];
  for(var p in dict){
     str.push(encodeURIComponent(p) + "=" + encodeURIComponent(dict[p]));
  }
  return str.join("&");
}

function updateError(xhr, status, error) {
    displayError('Status=' + xhr.status + ' (' + error + ')')
}

function displayError(message) {
    $("#error").html(message);
}



function updateGlobal(posts) {
    // Removes the old to-do list items
    $("div").each(
        function(){
            let my_id = parseInt(this.id.substring("id_post_".length))
            let id_in_posts = false
            $(posts).each(function(){
                if (this.id == my_id)
                    id_in_posts = true
            })
            if(!id_in_posts) this.remove
        })

    // Adds each new todolist item to the list (only if it's not already here)
    $(posts).each(function(){
        let my_id = "id_post_" + this.post_id
        if(document.getElementById(my_id) == null){
            let deleteButton
            if(this.user == myUserName){
                deleteButton = "<button onclick='deletePost(" + this.id + ")'>Delete</button>"
            }else{
                deleteButton = "<button style='visibility:hidden'>delete</button>"
            }

            $("#mainpost").append(
                '<div style="width: 70%;" class="mycontainer_light">' +
                deleteButton +
                '<div id="id_post_' + this.post_id + '" class="row">' +
                '        <span class="col-lg">Published by' +
                '            <p class="lead">\n' +
                '                <a href="profile/' + this.user + '">' +
                '                    <span class="message"' +
                '                          id="id_post_profile_' + this.post_id + '">' +
                                        this.first_name + " " + this.last_name +
                '                    </span>' +
                '                </a>' +
                '            </p>' +
                '            <p align="center">' +
                '                <span class="lead" id="id_post_text_'+ this.post_id + '">' +
                                    this.content + '</span>' +
                '            </p>' +
                '            <p align="right" class="small dark-teal-text h-50">' +
                '                <span id="id_post_date_time_'+ this.post_id +'">' +
                                    this.time +
                '                </span>' +
                '            </p>' +
                '        </span>' +
                '    </div class="commentarea">'+
                '        <div>' +
                '            <div class="col dark-teal-text">' +
                '                comment' +
                '            </div>' +
                '            <div>' +
                '                <input name="comment" class="form-control comment" id="id_comment_input_text_' + this.post_id + '" type="text">' +
                '            </div>' +
                '            <div align="right">' +
                '                <button id="id_comment_button_'+ this.post_id + '" onclick = "addcomment(' + this.post_id + ')" >Submit</button>' +
                '            </div>' +
                '        </div>'+
                '   </div>'
            )
        }
    })
}


function addcomment(post_id) {
    let tag = "#id_comment_input_text_" + post_id

    var comment_text = $(tag).val();

    // Clear input box and old error message (if any)
    $(tag).val('')
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment/" + post_id,
        type: "POST",
        data: "post_id=" + post_id + "&comment_text=" + comment_text+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: updatePage,
        error: updateError
    });
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

function addComment(content_text,postid){
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
    let urlcontent = {"content_text" : content_text, "post_id" : postid}

    request.open("POST", "/socialnetwork/add-comment/" + dictToURI(urlcontent), true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send("content="+postTextValue+"parentid="+postid+"&csrfmiddlewaretoken="+getCSRFToken());
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
    location.reload()
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
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

