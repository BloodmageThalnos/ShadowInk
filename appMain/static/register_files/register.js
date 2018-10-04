window.onload=function(){
    $('#huoQuY').click(function(){
        $.ajax({
            url:'/login/sendSMS',
            type:'POST',
            data:{
                "phone_number": $('#phoneNumber').val(),
            },
            success:function(data){
                //console.log(data)
            },
        })
    })
}