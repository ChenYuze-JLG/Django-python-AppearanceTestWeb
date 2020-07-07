// 定义视频流限制属性
var constraints = { video: { facingMode: "user" }, audio: false };

// 定义变量（video、img、canvas、capture）
const cameraView = document.querySelector("#video"),
      cameraOutput = document.querySelector("#img"),
      cameraSensor = document.querySelector("#canvas"),
      cameraTrigger = document.querySelector("#capture")

// 打开摄像头、获取视频流
function cameraStart() {
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function(stream) {
        track = stream.getTracks()[0];
        cameraView.srcObject = stream;
    })
    .catch(function(error) {
        console.error("错误！", error);
    });
}

// 拍照次数
var count = 0;

// 拍照函数
function triggerStart(){
    // 设置截图大小与视频流大小相同，videoWidth和videoHeight为可读值
    // cameraSensor.width = cameraView.videoWidth;
    // cameraSensor.height = cameraView.videoHeight;

    // 设置截图结果大小与视频当前大小相同，获取图片
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0, cameraView.width, cameraView.height);

    // 获取dataURL，质量为1
    dataURL = cameraSensor.toDataURL("image/webp", 1);
    // 将image文件地址设置为dataURL，由于初始无图片地址，改用默认图片
    // cameraOutput.src = dataURL;

    // 设置截图大小与视频相同
    cameraOutput.width = cameraView.width;
    cameraOutput.height = cameraView.height;
    count = count + 1;

    // 发送ajax请求，将dataURL信息和拍照次数count发送到后台
    $.ajax({
        async: true, // 这是开启异步请求, (默认值)
        url: "/app/video/ajax/", // 这是请求地址
        type: "post", // 提交数据的范式时post
        traditional: true,
        data: {'dataURL': dataURL, 'count': count},
        headers: {"X-CSRFToken":$.cookie("csrftoken")}, // 获取scrf_token
        success: function(data){
            if(data['state'] == "OK" && count == 5){
                cameraOutput.src = data['ResponseDataURL'];
                alert("识别成功!");
                var age=data['age'];
                var emoji=data['emoji'];
                var gender=data['gender'];
                var beauty=data['beauty'];
                var glaPoss=data['glaPoss'];
                var glaType=data['glaType'];
                var str1="<tr>"+"<td>"+age+"</td>"
                    +"<td>"+emoji+"</td>"
                    +"<td>"+gender+"</td>"
                    +"<td>"+beauty+"</td>"
                    +"<td>"+glaPoss+"</td>"
                    +"<td>"+glaType+"</td>"
                    +"</tr>"
                test.innerHTML=str1;
                ;

            }
            else if(data['state'] == "NO" && count == 5){
                alert("识别失败");
            }
        },
        error: function(data){
            if(count == 5){
                alert("提交失败");
            }
        }
    });
}

cameraTrigger.onclick = function(){
    count = 0;
    triggerStart();
    // 第一次拍照后，定义四个计时器，每过一秒拍一次
    var t1 = window.setTimeout(triggerStart, 1000);
    var t2 = window.setTimeout(triggerStart, 2000);
    var t3 = window.setTimeout(triggerStart, 3000);
    var t4 = window.setTimeout(triggerStart, 4000);
};

// 加载窗口时即获取视频流
window.addEventListener("load", cameraStart, false);
