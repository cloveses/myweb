% rebase('tpls/base.tpl')
<div class="pure-g">
<div class="pure-u-1-1" style="text-align: right;">{{info if info else ""}}
    %if name:
    <span style="margin-right: 1em;">你好，{{name}}</span>|
    <span style="margin:0 1em;"><a href="/chgpw/{{id}}">个人中心</a></span>|
    <span style="margin:0 1em;"><a href="/logout">退出</a></span>
    %else:
    <form action="" method="POST">
    姓名：<input type="text" name="name"  />
    密码：<input type="password" name="password" />
    验证：<input type="text" name="verify_text" />
    <img src="/verify" />
    <input type="submit" value="登录" />
    </form>
    %end
</div>
</div>

%if name:
    % include('tpls/nav.tpl',user_type=user_type)
%else:
    <div>
    <h2>易用内容管理系统说明</h2>
    <p>主要功能：</p>
    <p>分类管理</p>
    <p>用户管理</p>
    <p>用户权限管理</p>
    <p>内容管理</p>
    </div>
%end