% rebase('tpls/base.tpl')
<div>{{info if info else ""}}
    %if name:
    你好，{{name}}|<a href="/me/{{id}}">个人中心</a>|<a href="/logout">退出</a>
    %else:
    <form action="" method="POST">
    姓名：<input type="text" name="name"  />
    密码：<input type="password" name="password" />
    验证：<input type="text" name="verify_text" />
    <img src="/verify" />
    <input type="submit" value="登录" />
    </form>
    <a href="/signup">注册</a>
    %end
</div>

    % include('tpls/mnav.tpl',navs=navs)
    % for nav,news in newslist:
        <div style="border: 2px solid red;">
        {{nav.name}}<a href="/{{nav.id}}">更多</a>
        %for new in news:
            <li><a href="/news/{{str(new.id)}}{{'/'+plid if plid else ''}}" title="{{new.title}}">{{new.title}}</a></li>
        %end
        </div>
    %end
