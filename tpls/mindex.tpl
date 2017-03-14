% rebase('tpls/base.tpl')
<div class="pure-g">
<div class="pure-u-1-1" style="text-align: right;">
    {{info if info else ""}}
    %if name:
    <span style="margin-right: 1em;">你好，{{name}}</span>|
    <span style="margin:0 0.2em;"><a href="/me/{{id}}">个人中心</a></span>|
    <span style="margin:0 0.2em;"><a href="/logout">退出</a></span>
    %else:
    <form class="pure-form" action="" method="POST">
    姓名：<input type="text" name="name" size="6" placeholder="姓名" />
    密码：<input type="password" name="password" size="6" placeholder="密码" />
    验证：<input type="text" name="verify_text" size="6" placeholder="验证码" />
    <img src="/verify" height="35" style="vertical-align:middle;"/>
    <input type="submit" value="登录" class="pure-button" />
    <a href="/signup" class="pure-button">注册</a>
    </form>
    
    %end
</div>
</div>
<div class="pure-g">
<div class="pure-u-1-1 headimg">
</div>
</div>
    % include('tpls/mnav.tpl',navs=navs)

    %cols = 2
    %for i in range(0,len(newslist),cols):
    <div class="pure-g myclass">
        %for nav,news in newslist[i:i+cols]:
        <div class="pure-u-1-{{cols}}">
        <div class="mybox">
        <div>{{nav.name}}<a href="/{{nav.id}}" class="more">更多</a></div>
        %for new in news:
            <li>
                <a href="/news/{{str(new.id)}}{{'/'+plid if plid else ''}}" title="{{new.title}}">{{new.title}}</a>
                <span class="mydate">{{str(new.release_date)[:10]}}</span>
            </li>
        %end
        </div>
        </div>
        %end
    </div>
    %end