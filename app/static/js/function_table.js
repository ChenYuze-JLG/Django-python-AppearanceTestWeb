var show_table_button = document.querySelector("#show_table");

function get_data(){
    $.ajax({
        async: true, // 这是开启异步请求, (默认值)
        url: "/app/history/ajax/", // 这是请求地址
        type: "post", // 提交数据的范式时post
        traditional: true,
        data: { "flag": 0},
        headers: {"X-CSRFToken":$.cookie("csrftoken")}, // 获取scrf_token
        success: function(data){
            console.log("data:", data)
            if(data['state'] == "OK" ){
//                alert("数据获取成功!");
                var ID = data['ID'];
                var age=data['age'];
                var emoji=data['emoji'];
                var gender=data['gender'];
                var beauty=data['beauty'];
                var glaPoss=data['glaPoss'];
                var glaType=data['glaType'];
                var dateTime = data['dateTime'];
                var str_table = "";console
                for(var i = 0 ; i < age.length ; i++){
                    var str1="<tr>"
                        +"<td>"+age[i]+"</td>"
                        +"<td>"+emoji[i]+"</td>"
                        +"<td>"+gender[i]+"</td>"
                        +"<td>"+beauty[i]+"</td>"
                        +"<td>"+glaPoss[i]+"</td>"
                        +"<td>"+glaType[i]+"</td>"
                        +"<td>"+dateTime[i]+"</td>"
                        ;
                    // console.log(str_table);
                    var id = ID[i];
                    var button_temp = "<td>" + "<button class= 'btn  btn-lg active btn-warning' onclick='DeleteUserById("+id+")'>删除</button>" +"</td>"
                   // var button_temp = "<input type='button' onclick='app/DeleteUserById/ID[i]'>"
                     str_table = str_table + str1 + button_temp +"</tr>";
                    //  str_table = str_table + str1
                }
                test.innerHTML= str_table;
                console.log("hello")
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
     // $("#table_head").show();
     // console.log("hello")
     get_data();
};
