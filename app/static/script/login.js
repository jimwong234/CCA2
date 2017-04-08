/**
 * Created by jingwang on 2017-04-03.
 */
//once the document has loaded
$(document).ready(function(){
    //If this page was loaded after the user registered and was approved
    //(ie. the url includes "?approved=yes")
    if (window.location.href.indexOf("?approved=1") > -1){
        console.log("123");
        //Append the green approved check mark
        var $ApprovedTick = $('<img>',{ src: '../static/images/approved.svg',  //The image url
                                        alt: "Approved",
                                        width: '50px',
                                        id: 'RegistrationApproved'});

        //Append it to the header
        $('nav').append($ApprovedTick);
    }

});