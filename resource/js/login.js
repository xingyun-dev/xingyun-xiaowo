//注册：发送邮件
function doSendMail(obj) {
    var email = $.trim($('#regname').val());
    //对邮箱地址进行校验(xxx@xxx.xx)
    if (!email.match(/.+@.+\..+/)) {
        bootbox.alert({title: '错误提示', message: '邮箱地址格式不正确'});
        $('#regname').focus();
        return false
    }
    $.post('/ecode', 'email=' + email, function (data) {
        if (data == 'email-invalid') {
            bootbox.alert({title: '错误提示', message: '邮箱地址格式不正确'});
            $('#regname').focus();
            return false
        }
        if (data == 'send-pass') {
            bootbox.alert({title: '信息提示', message: '邮箱验证码已成功发送，请查收'});
            $('#regname').attr('disabled', true);  //验证码发送完成后禁止修改注册邮箱
            $(obj).attr('disabled', true);  //发送邮件按钮变成不可用
            return false
        } else {
            bootbox.alert({title: '错误提示', message: '邮箱验证码发送失败，请稍后再试'});
            return false
        }
    })
}

// 注册函数，包括获取地理位置信息
function doReg(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    regname = $.trim($("#regname").val());
    regpass = $.trim($("#regpass").val());
    regcode = $.trim($("#regcode").val());

    if (!regname.match(/.+@.+\..+/) || regpass.length < 5) {
        bootbox.alert({title: "错误提示", message: "注册邮箱不正确或密码少于5位"});
        return false;
    } else {
        // 获取地理位置信息
        getGeoLocationForRegistration(regname, regpass, regcode);
    }
}

// 修改后的注册函数，接受纬度和经度作为参数
function doRegWithGeo(regname, regpass, regcode, latitude, longitude) {
    var param = "username=" + regname;
    param += "&password=" + regpass;
    param += "&ecode=" + regcode;
    param += "&latitude=" + latitude; // 添加纬度参数
    param += "&longitude=" + longitude; // 添加经度参数
    //  // 创建一个URLSearchParams对象  
    // var param = new URLSearchParams();  
    // param.append('username', loginname);  
    // param.append('password', loginpass);  
    // param.append('vcode', logincode);  
      
    // // 如果经纬度是null，则添加"null"字符串，否则添加实际的值  
    // param.append('latitude', latitude !== null ? latitude : 'null');  
    // param.append('longitude', longitude !== null ? longitude : 'null');  
      
    // 将URLSearchParams对象转换为查询字符串  
    // var paramString = param.toString();  

    $.post('/user', param, function (data) {
        if (data == "ecode-error") {
            bootbox.alert({title: "错误提示", message: "验证码无效"});
            $("#regcode").val('');  // 清除验证码框的内容
            $("#regcode").focus();   // 让验证码框获取到焦点供用户输入
        } else if (data == "username-exist") {
            bootbox.alert({title: "错误提示", message: "该用户名已经被注册"});
            $("#regname").focus();
        } else if (data == "reg-pass") {
            bootbox.alert({title: "信息提示", message: "恭喜您,注册成功"});
            // 注册成功后,延迟1秒钟重新刷新当前页面
            setTimeout('location.reload();', 1000);
        } else if (data == "up-invalid") {
            bootbox.alert({title: "错误提示", message: "注册邮箱不正确或密码少于5位"});
        }
    });
}

// 调用函数以获取地理位置，并触发注册过程
function getGeoLocationForRegistration(regname, regpass, regcode) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
                doRegWithGeo(regname, regpass, regcode, latitude, longitude);
            },
            function (error) {
                console.error("获取地理位置失败: " + error.message);
                // 如果没有获取到位置信息，继续注册
                doRegWithGeo(regname, regpass, regcode, null, null);
            }
        );
    } else {
        console.error("浏览器不支持地理位置API");
        // 如果浏览器不支持，继续注册
        doRegWithGeo(regname, regpass, regcode, null, null);
    }
}


//重置密码：发送邮件
function SendMail(obj) {
    var email = $.trim($('#username').val());
    //对邮箱地址进行校验(xxx@xxx.xx)
    if (!email.match(/.+@.+\..+/)) {
        bootbox.alert({title: '错误提示', message: '邮箱地址格式不正确'});
        $('#username').focus();
        return false
    }
    $.post('/ecode', 'email=' + email, function (data) {
        if (data == 'email-invalid') {
            bootbox.alert({title: '错误提示', message: '邮箱地址格式不正确'});
            $('#username').focus();
            return false
        }
        if (data == 'send-pass') {
            bootbox.alert({title: '信息提示', message: '邮箱验证码已成功发送，请查收'});
            $('#username').attr('disabled', true);  //验证码发送完成后禁止修改注册邮箱
            $(obj).attr('disabled', true);  //发送邮件按钮变成不可用
            return false
        } else {
            bootbox.alert({title: '错误提示', message: '邮箱验证码发送失败，请稍后再试'});
            return false
        }
    })
}

//找回密码
function doReset(e) {
    //阻止回车键提交表单
    if (e != null && e.keyCode != 13) {
        return false;
    }
    username = $.trim($("#username").val());
    newpass = $.trim($("#newpass").val());
    findcode = $.trim($("#findcode").val());
    if (!username.match(/.+@.+\..+/) || newpass.length < 5) {
        bootbox.alert({title: "错误提示", message: "注册邮箱不正确或密码少于5位"});
        return false;
    } else {
        // 构建POST请求的正文数据
        param = "username=" + username;
        param += "&password=" + newpass;
        param += "&ecode=" + findcode;
        // 利用JQuery框架发送POST请求,并获取到后台注册接口的响应内容
        $.post('/reset', param, function (data) {
            if (data == "ecode-error") {
                bootbox.alert({title: "错误提示", message: "验证码无效"});
                $("#findcode").val('');  // 清除验证码框的内容
                $("#findcode").focus();   // 让验证码框获取到焦点供用户输入
            } else if (data == "user-not-found") {
                bootbox.alert({title: "错误提示", message: "邮箱地址还未注册，请先注册"});
                $("#username").focus();
            } else if (data == "reset-pass") {
                bootbox.alert({title: "信息提示", message: "恭喜您,密码重置成功"});
                // 注册成功后,延迟1秒钟重新刷新当前页面
                setTimeout('location.reload();', 1000);
            } else if (data == "up-invalid") {
                bootbox.alert({title: "错误提示", message: "邮箱不正确或重置密码少于5位"});
            }
        });
    }
}


// 显示模态框中的登录面板
function showLogin() {
    $("#login").addClass("active");
    $("#reg").removeClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").addClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").removeClass("active");
    $('#mymodal').modal('show');
}

// 显示模态框中的注册面板
function showReg() {
    $("#login").removeClass("active");
    $("#reg").addClass("active");
    $("#find").removeClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").addClass("active");
    $("#findpanel").removeClass("active");
    $('#mymodal').modal('show')
}


//  显示模态框中的找回密码面板
function showReset() {
    $("#login").removeClass("active");
    $("#reg").removeClass("active");
    $("#find").addClass("active");
    $("#loginpanel").removeClass("active");
    $("#regpanel").removeClass("active");
    $("#findpanel").addClass("active");
    $('#mymodal').modal('show');
}


//登录
function doLogin(e) {
    if (e != null && e.keyCode != 13) {
        return false;
    }

    var loginname = $.trim($("#loginname").val());
    var loginpass = $.trim($("#loginpass").val());
    var logincode = $.trim($("#logincode").val());
    if (loginname.length < 5 || loginpass.length < 5) {
        bootbox.alert({title: "错误提示", message: "用户名和密码少于5位."});
        return false;
    }else {
        // 获取地理位置信息
        getGeoLocationFordologin(loginname,loginpass,logincode);
    }
}

//修改后的登录函数，接受经度和维度作为参数
function dologinwithGeo(loginname,loginpass,logincode,latitude,longitude){
      // 构建POST请求的正文数据
    var param = "username=" + loginname;
    param += "&password=" + loginpass;
    param += "&vcode=" + logincode;
    param += "&latitude=" + latitude; // 添加纬度参数
    param += "&longitude=" + longitude; // 添加经度参数
    //  // 创建一个URLSearchParams对象  
    // var param = new URLSearchParams();  
    // param.append('username', loginname);  
    // param.append('password', loginpass);  
    // param.append('vcode', logincode);  
      
    // // 如果经纬度是null，则添加"null"字符串，否则添加实际的值  
    // param.append('latitude', latitude !== null ? latitude : 'null');  
    // param.append('longitude', longitude !== null ? longitude : 'null');  
      
    // // 将URLSearchParams对象转换为查询字符串  
    // var paramString = param.toString();  
    // 利用JQuery框架发送POST请求,并获取到后台注册接口的响应内容
    $.post('/login', param, function (data) {
        //
        if (data == "vcode-error") {
            bootbox.alert({title: "错误提示", message: "验证码无效."});
            $("#logincode").val('');  // 清楚验证码框的值
            $("#logincode").focus();   // 让验证码框获取到焦点供用户输入
        } else if (data == "login-pass") {
            bootbox.alert({title: "信息提示", message: "恭喜你,登录成功."});
            //登录成功后,延迟1秒刷新当前页面
//                setTimeout('location.reload();', 1000);
            // 登录成功后延迟1秒后跳转到指定URL
            setTimeout(function () {
                window.location.href = "/notebook"; // 替换为您想要跳转的URL
            }, 1000);

        } else if (data == "login-fail") {
            bootbox.alert({title: "错误提示", message: "登录失败,请联系管理员."});
        }
    });
}


// 调用函数以获取地理位置，并触发注册过程
function getGeoLocationFordologin(loginname,loginpass,logincode) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function (position) {
                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
               dologinwithGeo(loginname,loginpass,logincode, latitude, longitude);
            },
            function (error) {
                console.error("获取地理位置失败: " + error.message);
                // 如果没有获取到位置信息，继续登录
                dologinwithGeo(loginname,loginpass,logincode, null, null);
            }
        );
    } else {
        console.error("浏览器不支持地理位置API");
        // 如果浏览器不支持，继续登录
        dologinwithGeo(loginname,loginpass,logincode, null, null);

    }
}












//$(document).ready()是指页面加载即运行该代码
$(document).ready(function () {
    $.get('/loginfo', function (data) {
        content = '';
        if (data == null) {
            content += '<li class="nav-item"><a class="nav-link" href="#" onclick="showLogin()">登录</a></li>';
            content += '<li class="nav-item"><a class="nav-link" href="#" onclick="showReg()">注册</a></li>';
        } else {
            content += '<li class="nav-item"><a class="nav-link" href="/ucenter">欢迎您: ' + data["nickname"] + '</a>&nbsp;&nbsp;&nbsp;</li>'
            if (data['role'] == 'admin') {
                content += ' <li class="nav-item"><a class="nav-link" href="/admin">系统管理</a>&nbsp;&nbsp;&nbsp;</li>'
            } else {
                content += '<li class="nav-item"><a class="nav-link" href="/ucenter">个人中心</a>&nbsp;&nbsp;&nbsp;</li>'
            }
            content += ' <li class="nav-item"><a class="nav-link logout" onclick="confirmLogout()" href="#">退出</a></li>'
        }
        $("#loginmenu").append(content);
    })
})


//退出登录
function confirmLogout() {
    bootbox.confirm({
        title: "退出登录",
        message: "您确定要退出登录吗？",
        buttons: {
            confirm: {
                label: '确认',
                className: 'btn-success'
            },
            cancel: {
                label: '取消',
                className: 'btn-danger'
            }
        },
        callback: function (result) {
            if (result) {
                bootbox.alert({title: "信息提示", message: "已经退出登录！欢迎回来"});
                setTimeout(function () {
                    // 执行真正的退出登录操作
                    window.location.href = "/logout";
                }, 3000); // 3000毫秒即3秒
            }
        }
    });
}