"use strict"

function getGlobal() {
    $.ajax({
        url: "/socialnetwork/get-global-post",
        dataType : "json",
        success:  function (response) {
            updatePage(response,0)// global
        },
        error: updateError
    });
}

function getFollower() {
    $.ajax({
        url: "/socialnetwork/get-follower-post",
        dataType : "json",
        success: function (response) {
            console.log(response)
            updatePage(response,1)// Follower
        },
        error: updateError
    });
}

function getComment(post_id,page) {
    $.ajax({
        url: "/socialnetwork/get-comment/"+post_id,
        dataType : "json",
        success: function (response) {
            console.log(response)
            updatePageComment(response,post_id,page)// global
        },
        error: updateError
    });
}

function updatePage(response,page) {
    if (Array.isArray(response)) {
        updateGlobal(response,page)
    } else if (response.hasOwnProperty('error')) {
        displayError(response.error)
    } else {
        displayError(response)
    }
}


function updatePageComment(response,post_id,page) {
    if (Array.isArray(response)) {
        updateComment(response,post_id,page)
    } else if (response.hasOwnProperty('error')) {
        displayError(response.error)
    } else {
        displayError(response)
    }
}

function updateError(xhr, status, error) {
    displayError('Status=' + xhr.status + ' (' + error + ')')
}

function displayError(message) {
    $("#error").html(message);
}


function updateGlobal(posts,page) {
    // Removes the old to-do list items
    $(".mycontainer_light").each(
        function(){
            console.log(this.id)
            let my_id = parseInt(this.id.substring("id_post_".length))
            console.log(my_id)
            let id_in_posts = false
            $(posts).each(function(){
                if (this.post_id == my_id){
                    id_in_posts = true
                console.log("post" + this.post_id +"exists")
                }
            })
            if(!id_in_posts){
                this.remove()
                console.log("post" + this.post_id +"removes")
            }
        })

    // Adds each new todolist item to the list (only if it's not already here)
    $(posts).each(function(){
        let my_id = "id_post_" + this.post_id
        if(document.getElementById(my_id) == null){
            let deleteButton
            if(this.user == myUserName){
                deleteButton = "<button onclick='deletePost(" + this.post_id + ',' + page  +")'>Delete</button>"
            }else{
                deleteButton = "<button style='visibility:hidden'>delete</button>"
            }

            let commentarea
            if(page == 0){
                commentarea = '<div class="commentarea'+ this.post_id + '" id= "commentsforpost_'+ this.post_id + '"></div>'
            }else{
                commentarea = '<div class="commentarea_follower_'+ this.post_id + '" id= "commentsforpost_follower_'+ this.post_id + '"></div>'
            }

            $("#mainpost").prepend(
                '<div id="id_post_' + this.post_id + '"style="width: 70%;" class="mycontainer_light">' +
                deleteButton +
                '<div  class="row">' +
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
                                    sanitize(this.content) + '</span>' +
                '            </p>' +
                '            <p align="right" class="small dark-teal-text h-50">' +
                '                <span id="id_post_date_time_'+ this.post_id +'">' +
                                   parseDateTime(this.time) +
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
                '                <button id="id_comment_button_'+ this.post_id + '" onclick = "addcomment(' + this.post_id + ',' + page + ')" >Submit</button>' +
                '            </div>' +
                '        </div>'+
                commentarea +
                '   </div>'
            )
        }
        getComment(this.post_id,page)
    })
}


function updateComment(comments,post_id,page) {
    let commentareaId
    let commentclass

    if(page==0){
        commentareaId = "#commentsforpost_" + post_id
        commentclass = ".commentarea" + post_id + " .row "
    }else{
        commentareaId = "#commentsforpost_follower_" + post_id
        commentclass = ".commentarea_follower_" + post_id + " .row "
    }

    // let commentclass = ".commentarea" + post_id + " " + commentareaId  + " .row "
    console.log(commentclass)
    // Removes the old to-do list items
    $(commentclass).each(
        function(){
            console.log("this comment id is "+this.id+"\n")
            let my_id = parseInt(this.id.substring("id_comment_".length))
            console.log("my id = "+my_id+"\n")
            let id_in_comments = false
            $(comments).each(function(){
                console.log("comment each "+ this.comment_id +"\n")
                if (this.comment_id == my_id){
                    id_in_comments = true
                    console.log("comment "+ this.comment_id +" exists\n")
                }
            })
            if(!id_in_comments){
                console.log("comment  "+ this.id +"  remove\n")
                this.remove()
            }
        })

    // Adds each new todolist item to the list (only if it's not already here)
    $(comments).each(function(){
        let my_id = "id_comment_" + this.comment_id
        console.log("my_id = "+ my_id)
        if(document.getElementById(my_id) == null){
            let deleteButton
            if(this.commentuser == myUserName){
                deleteButton = "<button onclick='deleteComment(" + post_id + "," + this.comment_id + "," + page + ")'>Delete</button>"
            }else{
                deleteButton = "<button style='visibility:hidden'>delete</button>"
            }
            console.log("commentareaId---->"+ commentareaId)

            $(commentareaId).prepend(
                '<div id="id_comment_' + this.comment_id + '"class="row">' +
                '        <div class="col-2"></div>'+
                '<div class="col-10" >'+
                deleteButton +
                '            <div class="col-lg">Comment by' +
                '                <a href="profile/' + this.commentuser + '">' +
                '                <p class="lead">' +
                '                    <span class="commenter" id="id_comment_profile_' + this.comment_id + '">' + this.commentuser_firstname + " " + this.commentuser_lastname + '</span>' +
                '                    :' +
                '                </p>' +
                '               </a>'+
                '                <p align="center">' +
                '                    <span class="lead" id="id_comment_text_' + this.comment_id + '">' + sanitize(this.commentcontent) + '</span>' +
                '                </p>' +
                '                <p align="right" class="small dark-teal-text">\n' +
                '                    <span id="id_comment_date_time_' + this.comment_id + '">' + parseDateTime(this.commenttime) + '</span>' +
                '                </p>' +
                '            </div></div></div></div>'
            )
        }
    })
}


function addPost(){
    let postTextElement = document.getElementById("id_post_input_text")
    let postTextValue = postTextElement.value

    // Clear input box and old error message (if any)
    postTextElement.value = "";
    displayError("");

    $.ajax({
        url: "/socialnetwork/makepost" ,
        type: "POST",
        data: "post=" + postTextValue +"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function (response) {
            updatePage(response,0)
        },
        error: updateError
    });
}

function deletePost(id,page) {

    $.ajax({
        url: "/socialnetwork/delete-post/"+id,
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response){
            console.log("deletePost"+id),
            updatePage(response,0)
        },
        error: updateError
    });
}

function addcomment(post_id,page) {
    let tag = "#id_comment_input_text_" + post_id
    var comment_text = $(tag).val();
    console.log("comment input visiting is:    "+tag)

    // Clear input box and old error message (if any)
    $(tag).val('')
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment",
        type: "POST",
        data: "post_id=" + post_id + "&comment_text=" + comment_text+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function (response) {
            updatePageComment(response,post_id,page)
        },
        error: updateError
    });
}

function deleteComment(post_id,comment_id,page) {

    $.ajax({
        url: "/socialnetwork/delete-comment/" + comment_id,
        type: "POST",
        data: "csrfmiddlewaretoken="+getCSRFToken(),
        dataType : "json",
        success: function(response){
            console.log("deletecomment "+ comment_id +" in mainpost "+ post_id)
            updatePageComment(response, post_id,page)
        },
        error: updateError
    });
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            // .replace(/&#63/g, '&quest;')
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

function parseDateTime(isotime){
    let datetime = new Date(isotime.toString())
    var amOrPm = (datetime.getHours() < 12) ? "AM" : "PM";
    var hour = (datetime.getHours() < 13) ? datetime.getHours() : datetime.getHours() - 12;
    let datetimestring = datetime.getMonth()+1 + '/' + datetime.getDate() + '/' + datetime.getFullYear() + ' ' + hour + ':' + datetime.getMinutes() + ' ' + amOrPm;
    return datetimestring
}

