<%-- 
    Document   : IPFinder
    Created on : 2018-9-15, 22:18:33
    Author     : dell
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@ page import="java.io.*,java.util.*" %>
<%@ page import="toolsing.NetWorkUtil" %>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
        <h1>Hello World!</h1>
        <% out.print(NetWorkUtil.getIpAddress(request)); %>
    </body>
</html>
