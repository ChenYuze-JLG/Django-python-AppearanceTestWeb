var show_rank_button = document.querySelector("#show_rank");

function getRankData(){
    $.ajax({
        async: true, // 这是开启异步请求, (默认值)
        url: "/app/history/rank/", // 这是请求地址
        type: "post", // 提交数据的范式时post
        traditional: true,
        data: {"flag": 0},
        headers: {"X-CSRFToken":$.cookie("csrftoken")}, // 获取scrf_token
        success: function(data){
            if(data['state'] == "OK" ){
                //alert("数据获取成功!");
                var name=data['name'];
                var score=data['score'];
                var str_table = "";
                for(var i = 0 ; i < name.length ; i++){
                    var str="<tr>"
                        +"<td>"+String(i+1)+"</td>"
                        +"<td>"+name[i]+"</td>"
                        +"<td>"+score[i]+"</td>"
                        +"</tr>";
                    str_table = str_table + str;
                }
                rank_table.innerHTML= str_table;
                console.log("hello");
            }
            else if(data['state'] == "NO" ){
                //alert("数据获取失败");
            }
        },
        error: function(data){
            //alert("数据获取失败");
        }
    });
}

show_rank_button.onclick = function(){
    getRankData();
}
