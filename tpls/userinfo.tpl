<div class="pure-g">
<div class="pure-u-1-1" style="text-align: right;">
    {{info if 'info' in locals() and info else ""}}
    %if name:
    <span style="margin-right: 1em;">你好，{{name}}</span>|
    <span style="margin:0 1em;"><a href="/chgpw/{{id}}">个人中心</a></span>|
    <span style="margin:0 1em;"><a href="/logout">退出</a></span>
    %else:
    <form  class="pure-form" action="" method="POST">
    姓名：<input type="text" name="name" size="6"/>
    密码：<input type="password" name="password" size="6"/>
    验证：<input type="text" name="verify_text" size="6"/>
    <img src="/verify" height="35" style="vertical-align:middle;" />
    <input type="submit" value="登录" />
    </form>
    %end
</div>
</div>