$(document).ready( function(){

    $("#email").focusout( function(){
        console.log("focusout")
        verificarEmail(false)
    })

    //$("[id^=btn-submit-]").click( function(){
    $("#btn-submit-datagral").click( function(){
        if(verificarEmail(true) == false){
            return false;
        }
    })

    $(window).keydown(function(event){ //prevent users hitting click and submmitting
        if(event.keyCode == 13) {
          event.preventDefault();
          return false;
        }
    });

})

function eraseErrores(){
    $(".ajax-err").remove();
}  

function renderErrorIn(elId,errores){
    txt = "" 
    i = 0
    for (var error in errores){
        txt += "<li class='error err'>" + errores[error] + "</li>"
        i++
    }
    if (i > 0){
        $("#"+elId).after("<ul class='ajax-err messages'>" + txt + "</ul>")
    }
}  


function verificarEmail(presionado){
    
    var data = $("#form_datagral").serialize();

    $.ajax({
        type:"POST",
        url: "/register/checkEmail",
        data: data,
        dataType:"JSON",
    })
    .done( function(response){
        //console.log(response)
        //error = response["errors"]
        //console.log("PRESIONADO=" + presionado + "; SIZE =" + Object.keys(response).length) 
        var size = Object.keys(response).length;
        eraseErrores()
        if(size == 0){
            if (presionado == true){
                $("#form_datagral").submit();
            }
        } else {
            renderErrorIn("email",response)
        }
    })
    .fail( function(){
        alert("FALLA...")
    })
    .always( function(){
        //nada
    })
    return false
};

//DIRECT JAVASCRIPT
function chkErrores(elId) {

    var x = document.getElementById(elId);
    var valor = x.value
    var errores = []
    switch(elId){
        //[via AJAX ]case "email":
        case "first_name":
            if (valor.length == 0){
                errores.push("First name is required!")
            }
            else if (valor.length < 2 | valor.length > 100){
                errores.push("First name must be between 2 to 100 characters")
            }
            break;
        case "last_name":
            if (valor.length == 0){
                errores.push("Last name is required!")
            } else if (valor.length < 2 | valor.length > 100){
                errores.push("Last name must be between 2 to 100 characters")
            }
            break;
        case "password":
            if (valor.length == 0){
                errores.push("Password is required!")
            } else if (valor.length < 8){
                errores.push("Password must have at least 8 characters")
            }
            break;
        case "confirm_password":
            var pass = document.getElementById("password").value
            if (valor.length == 0){
                errores.push("Please confirm password!")
            } else if (pass != valor){
                errores.push("Confirmed password does not match with given password!")
            }
            break;
    }

    if (errores.length > 0){
        txt = "" 
        i = 0
        for (var error in errores){
            txt += "<li class='error err'>" + errores[error] + "</li>"
            i++
        }
        if (i > 0){
            $("#"+elId).after("<ul class='err_"+elId+"'>" + txt + "</ul>")
        }
    }
    
}

function eraseError(elId){
    $(".err_"+elId).remove();
}  
