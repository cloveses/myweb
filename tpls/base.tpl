<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <script language="javascript" type="text/javascript" src="/static/jquerymin.js"></script>
    <link rel="stylesheet" type="text/css" href="/static/main.css" />
    <link rel="stylesheet" type="text/css" href="/static/purecss/base-min.css" />
    <link rel="stylesheet" type="text/css" href="/static/purecss/pure-min.css" />
    <title>易用内容管理系统</title>
</head>
<body style="background-color:#FFF;">
<div id="mybody">
{{!base}}
</div>
<div class="pure-g">
    <div class="pure-u-1-1" style="text-align: center;">
        <footer>&copy;2017 宿州环保工程学校 刘海名师工作坊</footer>
    </div>
</div>
<script type="text/javascript">
    function display_img(){
            $("#verify_text").after("<img src='/verify' height='35' style='vertical-align:middle;'/>");
            $("body").off("focus","#verify_text");
        }
    $(function(){
        $("body").on("focus","#verify_text",display_img);
    });
</script>
</body>
</html>