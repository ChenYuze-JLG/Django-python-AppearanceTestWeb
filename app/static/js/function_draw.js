var show_curve_button = document.querySelector("#show_curve");

//声明全局颜值变量
var nums = [];   // 颜值
var datas = [];  // 日期
var flag = 0;
function getData(){
    // 这里是用于测试
    nums = [77, 65, 34, 56, 98];
    datas = ["11.1-11.2", "11.3-11.9", "11.10-11.16",
            "11.17-11.23", "11.24-11.30"];
    flag = 0;
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
                nums = data['beauty'];
                datas = data['dateTime'];
                for(var i=0; i<datas.length; i++){
                    var s1 = datas[i].slice(0, 10);
                    var s2 = datas[i].slice(11, 19);
                    datas[i] = s1 + "\n" + s2 + "\n";
                }
                flag = 1;
            }
            else if(data['state'] == "NO" ){
//                alert("数据获取失败");
            }
        },
        error: function(data){
//            alert("数据获取失败");
        }
    });
}
getData();
show_curve_button.onclick = function(){
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('can1'));

    // 指定图表的配置项和数据
    var option = {
        title: {
            text: '历史颜值数据'
        },
        tooltip: {},
        legend: {
            data:['颜值评分']
        },
        xAxis: {
            data: datas
        },
        yAxis: {},
        dataZoom: [
            {
                type: 'inside', // 这个 dataZoom 组件是 inside 型 dataZoom 组件
                start: 10,      // 左边在 10% 的位置。
                end: 40         // 右边在 40% 的位置。
            }
        ],
        series: [{
            name: '颜值评分',
            type: 'line',
            data: nums
        }],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            },
            backgroundColor: 'rgba(245, 245, 245, 0.8)',
            borderWidth: 1,
            borderColor: '#ccc',
            padding: 10,
            textStyle: {
                color: '#000'
            },
            position: function (pos, params, el, elRect, size) {
                var obj = {top: 10};
                obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                return obj;
            },
            extraCssText: 'width: 170px'
        },
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}



