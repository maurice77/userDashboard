
$(document).ready( function(){

    var miEl = document.getElementById("removeModal")

    miEl.addEventListener('hide.bs.modal', function (event) {

        var button = event.target; 

        console.log(button)
    })

    miEl.addEventListener('show.bs.modal', function (event) {      
        var button = event.relatedTarget;
        
        user_id = button.id

        $("#id-to-remove").val(user_id)
        $(".modal-body").html(`Confirm to remove user ${user_id}?`);

    })  

    $('#modal-remove-btn').on('click', function() {
        //alert(`Remove now ${ $("#id-to-remove").val() }!!`);
        removeUser($("#id-to-remove").val());
        $('#removeModal').modal('hide');
    });

})

function removeUser(id_user){

    $.ajax({
        type:"GET",
        url: `/users/remove/${id_user}`,
        dataType:"JSON",
    })
    .done( function(response){
        console.log("ajax.done")
        if (response["deleted"]){
            //del msg in template
            $("#tr-"+id_user).remove();
        } else {
            if ("deleted" in response){
                alert(`ERROR: Cannot delete this user.`)
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
