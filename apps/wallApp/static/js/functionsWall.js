
$(document).on("click", "[id^=btn-delete-msg]", function(){
    console.log("deleting msg with click!")
    id = $(this).attr('id').substring(15)
    deleteMessage(id)
    return false;
});

$(document).on("click", "[id^=btn-delete-com]", function(){
    console.log("deleting comment with click!")
    id = $(this).attr('id').substring(15)
    deleteComment(id)
    return false;
});

$(document).on("click","[id^=btn-submit-comment]", function(){
    console.log("posting comment with click!")
    id = $(this).attr('id').substring(19)
    if (document.getElementById("comment-"+id).value != ''){
        postComment(id)
    };
    return false;
})

$(document).ready( function(){

    $("#btn-submit-message").click( function(){
        if (document.getElementById("message").value != ''){
            postMessage()
        }
        return false;
    })


})

function updateCreatedAt(){
    $.ajax({
        type:"GET",
        url: "/users/show/get_created_at",
        dataType:"JSON",
    })
    .done( function(response){

        //devuelve messages y comments
        for (var key in response["messages"]){
            //console.log($("#span-msg-"+key))
            //console.log(key + " - " + response.messages[key]["created_at"])
            $("#span-msg-"+key).text(response.messages[key]["created_at"])
            //document.getElementById("span-msg-"+key).innerHTML = response.messages[key]["created_at"]
            if (response.messages[key]["minutes"] > 30){
                if ( $( "#btn-delete-msg-"+key ).length ) {
                    document.getElementById("btn-delete-msg-"+key).remove();
                }
            } else {
                $("#btn-delete-msg-"+key).show(); 
            }
        }
        //misMessages = ($("[id^=span-msg]"))
        //for (var i; misMessages.length; i++ ){
        //    key = ""
        //   misMessages[i].textContent = ""
        //}

        for (var key in response["comments"]){
            //console.log(key + " - " + response.messages[key]["created_at"])
            $("#span-com-"+key).text(response.comments[key]["created_at"])
            if (response.comments[key]["minutes"] > 30){
                if ( $( "#btn-delete-com-"+key ).length ) {
                    $("#btn-delete-com-"+key).remove();
                }
            } else {
                $("#btn-delete-com-"+key).show();
            }
        }

    })
    .fail( function(){
        alert("FALLA...")
    })
    .always( function(){
        //nada
    })

}

function postComment(idMsg){

    var data = $("#form-comment-"+idMsg).serialize();
    var token = data.substring(20,data.indexOf("&comment="))

    $.ajax({
        type:"POST",
        url: "/users/show/post_comment",
        data: data,
        dataType:"JSON",
    })
    .done( function(response){
        var size = Object.keys(response).length;
        
        if (size > 0){
            txt =`<div id="divcomment-${response.id}" class="comment-i">
                    <div class="postedby-erase">
                        <p class="posted_by msg-header">${response.user.full_name} - <span id="span-com-${response.id}">Posteado hace menos de un minuto</span></p>   
                        <form action="/wall/delete_comment" id="form-com-${response.id}" method="POST" class="msg-header">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${token}">
                            <button id="btn-delete-com-${response.id}"
                            class="btn btn-outline-secondary btn-sm btn-erase-com">Erase</button>
                            <input type="hidden" name="comment_id" value=${response.id}>
                            <input type="hidden" name="tipo" value="js"}>
                        </form>
                    </div>
                    <p>${response.comment}</p>
                </div>`

            $( "#form-comment-"+idMsg).before( txt );
            $( "#comment-"+idMsg).val(''); //remove post from textarea
        } else {
            console.log("Message cannot be added to DB")
        }
    })
    .fail( function(){
        alert("FALLA...")
    })
    .always( function(){
        //nada
    })

}

function postMessage(){

    var data = $("#form-message").serialize();
    var token = data.substring(20,data.indexOf("&message="))

    $.ajax({
        type:"POST",
        url: "/users/show/post_message",
        data: data,
        dataType:"JSON",
    })
    .done( function(response){
        var size = Object.keys(response).length;

        if (size > 0){
            //console.log(response)
            //document.getElementById("divmessage-"+msgId).remove();

            txt = `<div class="message" id="divmessage-${response.id}">
                <div class="postedby-erase">
                    <p class="posted_by msg-header">${response.user.full_name} - <span id="span-msg-${response.id}">Posteado hace menos de un minuto</span></p>
                    <form action="/wall/delete_message" id="form-msg-${response.id}" method="POST" class="msg-header">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${token}">
                        <input type="hidden" name="message_id" value="${response.id}">
                        <input type="hidden" name="tipo" value="js"}>
                        <button id="btn-delete-msg-${response.id}" value="${response.id}"
                        class="btn btn-outline-dark btn-sm btn-erase-msg">Erase</button><!--onclick="deleteMessage(${response.id})"-->
                    </form>
                </div>  
                <p>${response.message}</p>
                <div class="comment">
                    <form action="/wall/post_comment" id="form-comment-${response.id}" method="POST">
                        <input type="hidden" name="csrfmiddlewaretoken" value="${token}">
                        <div class="form-floating">
                            <textarea class="form-control" placeholder="Comments" id="comment-${response.id}" 
                            name="comment" style="height:100px;" ></textarea>
                            <label for="comment-${response.id}">Post a comment...</label>
                        </div>
                        <input type="hidden" value=${response.id} name="message_id">
                        <input type="hidden" name="tipo" value="js"}>
                        <div class="row mgt-1">
                            <div class="col-10">
                                <button id="btn-submit-comment-${response.id}" class="btn btn-primary">Post comment!</button>
                            </div>
                        </div> 
                    </form>
                </div>
            </div>`

            $( "#post-msg-below" ).after( txt );
            $( "#message").val(''); //remove post from textarea

        } else {
            console.log("Message cannot be added to DB")
        }
    })
    .fail( function(){
        alert("FALLA...")
    })
    .always( function(){
        //nada
    })

}

function deleteMessage(msgId){

    var data = $("#form-msg-"+msgId).serialize();

    $.ajax({
        type:"POST",
        url: "/users/show/delete_message",
        data: data,
        dataType:"json",
    })
    .done( function(response){
        console.log("ajax.done")
        if (response["deleted"]){
            //del msg in template
            document.getElementById("divmessage-"+msgId).remove();
        } else {
            if ("deleted" in response){
                alert("ERROR: No es posible borrar el mensaje ya que han pasado mas de 30 minutos desde que se posteó.")
            } else {
                console.log("Element cannot be erased from DB")
            }
        }
    })
    .fail( function(){
        alert("FALLA...")
    })
    .always( function(){
        //nada
    })

}

function deleteComment(comId){

    var data = $("#form-com-"+comId).serialize();

    $.ajax({
        type:"POST",
        url: "/users/show/delete_comment",
        data: data,
        dataType:"JSON",
    })
    .done( function(response){
        if (response["deleted"]){
            //del com in template
            document.getElementById("divcomment-"+comId).remove();
        } else {
            if ("deleted" in response){
                alert("ERROR: No es posible borrar el comentario ya que han pasado mas de 30 minutos desde que se posteó.")
            } else {
                console.log("Element cannot be erased from DB")
            }
        }
    })
    .fail( function(){
        alert("FALLA...")
    })
    .always( function(){
        //nada
    })
}