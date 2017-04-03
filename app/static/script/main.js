/**************************************New JQuery Lib Code*****************************************/

//once the document has loaded
$.noConflict();

//Replace all $ with jQuery

$(document).ready
(
    function()
    {
 
         //First thing is to check and see if the user was previously logged in
         jQuery.ajax({
                        type: 'GET',
                        url: "/WasUserLoggedIn",
                        dataType: 'text',
                        success: function (response)
                        {
                            if(response == 'userwasloggedin')
                                //Go back to home page
                                window.location.replace("/Profile_SelfView.html");
                        }
                     }); //End of AJAX
    }

);

/* Jim's responsive design start here*/
function showNavBtn(){
    var width = window.innerWidth;
    if(width <= 740){
        var x = document.getElementById("Main_Nav");
        if(x.className == "main_navs"){
            x.className += "_responsive";
        }else {
            x.className = "main_navs";
        }
        x = document.getElementById("Home_Buttons");
        if(x.className == "home_btns"){
            x.className += "_responsive";
        }else {
            x.className = "home_btns";
        }
    }
}
/* Jim's responsive design end here*/



