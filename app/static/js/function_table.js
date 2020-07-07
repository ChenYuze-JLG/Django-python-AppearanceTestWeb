var show_table_button = document.querySelector("#show_table");

function get_data(){
    $.ajax({
        async: false, // 这是开启异步请求, (默认值)
        url: "/app/history/ajax/", // 这是请求地址
        type: "post", // 提交数据的范式时post
        traditional: true,
        data: {"flag": flag},
        headers: {"X-CSRFToken":$.cookie("csrftoken")}, // 获取scrf_token
        success: function(data){
            if(data['state'] == "OK" ){
//                alert("数据获取成功!");
                var age=data['age'];
                var emoji=data['emoji'];
                var gender=data['gender'];
                var beauty=data['beauty'];
                var glaPoss=data['glaPoss'];
                var glaType=data['glaType'];
                var str_table = "";
                for(var i = 0 ; i < age.length ; i++){
                    var str1="<tr>"
                        +"<td>"+age[i]+"</td>"
                        +"<td>"+emoji[i]+"</td>"
                        +"<td>"+gender[i]+"</td>"
                        +"<td>"+beauty[i]+"</td>"
                        +"<td>"+glaPoss[i]+"</td>"
                        +"<td>"+glaType[i]+"</td>"
                        +"</tr>";
                    console.log(str_table);
                    str_table = str_table + str1;
                }
                test.innerHTML= str_table;
            }
            else if(data['state'] == "NO" ){
//                alert("数据获取失败");
            }
        },
        error: function(data){
//                alert("数据获取失败");
        }
    });
}

show_table_button.onclick = function(){
//    $("#table_head").show();
    get_data();
}
