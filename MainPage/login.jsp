<%-- 
    Document   : login
    Created on : 2018-9-16, 13:56:16
    Author     : dell
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html" charset="UTF-8">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <title>墨影</title>
        <meta id="viewport" name="viewport" content="width=device-width,initial-scale=1.0,minimum-scale=1.0,maximum-scale=1.0,minimal-ui">
        <link rel="stylesheet" href="./login_files/login.css">
        <script type="text/javascript" src="./login_files/patternLock.min.js" charset="utf-8"></script>
    </head>
    <body style="height:100%">
            <style type="text/css">
                    body{
                            background-image:url(./bk.jpg);
                            background-size:cover;
                    }
            </style>
    <div class="login-wrapper" id="loginWrapper" style="display: block; min-height: initial;">
        <section class="avatar-wrapper" id="avatarWrapper">
            <img src="./icon.png">
            </section>
        <form id="loginForm" action="/login" method="POST">
            <div class="box">
                <div class="input-wrapper">
                    <i class="icon forName"></i>
                    <!-- 用户名 -->
                    <p class="input-box">
                        <input type="text" placeholder="用户名/手机号" id="loginName" name="name">
                        <!-- 清除用户名小叉 -->
                        <a href="javascript:;" class="input-clear hid" id="loginnameclear"></a>
                    </p>
                </div>
                <div class="input-wrapper">
                    <i class="icon forPwd"></i>
                    <p class="input-box">
                    <input type="password" placeholder="请输入密码" id="loginPassword" name="password">
                    </p>
                </div>
            </div>
            <a href="javascript:document.getElementById('loginForm').submit()" class="btn btnRed" id="loginAction">登陆</a>
        </form>
        <footer class="footer">
            <a href="/register">注册账号</a><a href="">忘记密码</a>
        </footer>
</body>
</html>
