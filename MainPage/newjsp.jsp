<%-- 
    Document   : newjspidnex
    Created on : 2018-9-14, 14:56:32
    Author     : shao
--%>

<%@page import="toolsing.NetWorkUtil"%>
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page import="java.io.*,java.util.*" %>
<%@ page import="java.math.BigInteger" %>
<%
    String title = "UserName Example";
%>
<%! BigInteger times=new BigInteger("2");%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title><% out.print(title); %></title>
    </head>
    <body>
    
    <center>
    <h1><% out.print((new Date()).toLocaleString()); %></h1>
    </center>
    
    
        <h2 style="word-break:break-all">
            
            <% times=times.multiply(times);%>
            <% out.println(times);%>
        </h2>
    
    <script>
            location.reload();
    </script>
    </body>
</html>