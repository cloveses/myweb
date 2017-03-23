<div class="pure-g">
<div class="pure-u-1-1" style="text-align: right;">
    {{info if 'info' in locals() and info else ""}}
    %if name:
    <span style="margin-right: 1em;">你好，{{name}}</span>|
    <span style="margin:0 1em;"><a href="/chgpw/{{id}}">个人中心</a></span>|
    <span style="margin:0 1em;"><a href="/adlogout">退出</a></span>
    %else:
    <form  class="pure-form" action="" method="POST">
    姓名：<input type="text" name="name" size="6" placeholder="姓名" />
    密码：<input type="password" name="password" size="6" placeholder="密码" />
    验证：<input type="text" id="verify_text" name="verify_text" size="6" placeholder="验证码" />
    <input type="submit" value="登录" class="pure-button" />
    </form>
    %end
</div>
</div>