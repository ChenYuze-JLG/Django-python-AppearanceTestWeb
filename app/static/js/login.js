
$(function () {
    $('.tab-menu li').click(function () {
        $(this).addClass('active').siblings().removeClass('active');
//          $('.tab-top li').eq($(this).index()).addClass('active').siblings().removeClass('active');  tab按钮第二种写法
        var index = $(this).index();
        $(".tab-con div").eq(index).show().siblings().hide();
    });
});

$(function () {
    // ajax 刷新验证码
    $('.captcha').click(function () {
        console.log('click');
        $.getJSON("/captcha/refresh", function (result) {
            $('.captcha').attr('src', result['image_url']);
            $('#id_captcha_0').val(result['key'])
        });
    });
})

function checkPwd() {
    var pwd1 = document.getElementById("password1").value;
    var pwd2 = document.getElementById("passwordAgain").value;
    var us = document.getElementById("username1").value;
    console.log(pwd1);
    var pwdSpan = document.getElementById("pwdSpan");

    if ((pwd1 !== pwd2) || (pwd1.length == 0)) {
        pwdSpan.innerHTML = "<font color = 'red' font-size = 32px>×</font>";
        $("#btnSub").attr('disabled', true);
    } else {
        pwdSpan.innerHTML = "<font color = 'green' font-size = 32px>√</font>";
        $("#btnSub").attr('disabled', false);
    }
}

function msg() {
    var msg = document.getElementById('msgRegister').innerText.trim();
    console.log(msg);
    if (msg !== "") {
        alert(msg);
    }
}

msg();


function usernameAjax() {
    // 通过ajax发送发送到后台进行验证用户名的唯一性
    var username = document.getElementById('username1').value;
    $.ajax({
        async: true, // 这是开启异步请求, (默认值)
        url: "/app/register/ajax/" + username, // 这是请求地址
        type: "post", // 提交数据的范式时post
        headers: {"X-CSRFToken": $.cookie("csrftoken")}, // 获取scrf_token
        success: function (data) {
            // 这里时服务器成功处理请求, 并且返回数据
            if (data['username'] === "False") {
                document.getElementById("checkUsername").innerHTML = "该用户名已被使用";

                document.getElementById("checkUsername").style.display = "block";
            } else {
                document.getElementById("checkUsername").innerHTML = null;

                document.getElementById("checkUsername").style.display = "none";
            }
        },
    });
}