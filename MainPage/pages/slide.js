!function(){
    
    turn=0
    pic_number=3
    function slide(){
        turn+=103
        Css = {'transform':("translate(-"+turn+"%,0)"), 'transition': 'all 0.8s ease-out'};
        for(i=1;i<=pic_number*2;i++)
            $('#img'+i).css(Css);
        
        if(turn==309)setTimeout(function(){
        turn=0
        Css = {'transform':("translate(0,0)"), 'transition': 'all 0.0s ease-out'};
        for(i=1;i<=pic_number*2;i++)
            $('#img'+i).css(Css);
        },800)
    }

    setInterval(slide,1500)

}();