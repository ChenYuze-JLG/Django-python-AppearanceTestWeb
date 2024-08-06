var show_curve_button = document.querySelector("#show_curve");

var nums = new Array();
var datas = new Array();
//声明全局颜值变量

show_curve_button.onclick = function(){
    getData();
}

function getData(){
    $.ajax({
        async: true, // 这是开启异步请求, (默认值)
        url: "/app/history/ajax/", // 这是请求地址
        type: "post", // 提交数据的范式时post
        traditional: true,
        data: {"flag": 0},
        headers: {"X-CSRFToken":$.cookie("csrftoken")}, // 获取scrf_token
        success: function(data){
            if(data['state'] == "OK" ){
                nums = data['beauty'];
                datas = data['dateTime'];
                for(var i=0; i<datas.length; i++){
                    var s1 = datas[i].slice(0, 10);
                    var s2 = datas[i].slice(11, 19);
                    datas[i] = s1 + "\n" + s2 + "\n";
                }
                draw();
            }
            else if(data['state'] == "NO" ){
                alert("数据获取失败");
            }
        },
        error: function(data){
            alert("数据获取失败");
        }
    });
}

function draw(){
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('can1'));
    var l = 0;
    var r = 100;
    if(datas.length > 10){
        r = 1000 / datas.length;
    }
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
                start: l,      // 左边在 l 的位置。
                end: r         // 右边在 r 的位置。
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


