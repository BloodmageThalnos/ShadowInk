window.onload=function(){
    $('#huoQuY').click(function() {
        $.ajax({
            url: '/login/sendSMS',
            type: 'POST',
            data: {
                "phone_number": $('#phoneNumber').val(),
            },
            success: data => {
                console.log(data)
            },
        })
        $('#huoQuY').text('发送成功')
        $('#huoQuY').attr('disabled','disabled')
        window.timer_t=20
        window.timer_i=window.setInterval(function(){
            $('#huoQuY').text('重新发送('+window.timer_t+')')
            if(--window.timer_t<0){
                window.timer_i=window.clearInterval(window.timer_i)
                $('#huoQuY').text('发送验证码')
                $('#huoQuY').removeAttr('disabled')
            }
        },1000)
    })
}
