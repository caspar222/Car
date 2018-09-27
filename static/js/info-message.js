$(function(){
    var move=0;
    var $point=$(".point");
    var $form=$(".contain>.form");
    //点击下一步
    $(".next").click(function(e){
        $tar=$(e.target);
        move++;//1
        $(".prev").removeAttr("disabled");//move大于1的时候  上一页可用
        //小于move的变成绿色
        $point.children(":lt("+move+")").find("b").css("background-color","#10C642")
        //等于move的变成橙色
        $point.children(":eq("+move+")").find("b").css("background-color","#FF8F03")
        console.log(move);

        if(move==4){
               $tar.html("提交");
        }else if(move==5){
            $tar.attr("type","submit")
        }
        $form.children("div:eq("+move+")").css("display","block").siblings("div").css("display","none");
    });

    //点击上一步
    $(".prev").click(function(e){
        $tar=$(e.target);
        move--;
        if(move<=0){//move小于或者等于0时，上一页不可用
            $tar.attr("disabled",true);
        }
        $(".next").html("下一步");
        $point.children(":gt("+move+")").find("b").css("background-color","#DEDCD8");
        $point.children(":eq("+move+")").find("b").css("background-color","#FF8F03");
        $form.children("div:eq("+move+")").css("display","block").siblings("div").css("display","none");
        console.log(move);
    });
});





