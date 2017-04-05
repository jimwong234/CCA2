/**
 * Created by jingwang on 2017-04-04.
 */
$(document).ready(function () {
    $('#file-input').change(function () {
        $('#UploadProfilePic').submit();
    });
    $(document).on('click','#SignOut_Button',function(){
        $.ajax({
            type:'GET',
            url:'/signout',
            dataType:'text',
            success: function (response){
                window.location.replace("/");
            }
        });
    });
});