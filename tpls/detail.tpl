% rebase('tpls/base.tpl')
<div class="pure-g">
<div class="pure-u-1-1" style="text-align: right;">
    {{info if 'info' in locals() and info else ""}}
    %if name:
    <span style="margin-right: 1em;">你好，{{name}}</span>|
    <span style="margin:0 0.2em;"><a href="/me/{{id}}">个人中心</a></span>|
    <span style="margin:0 0.2em;"><a href="/logout">退出</a></span>
    %else:
    <form class="pure-form" action="/" method="POST">
    姓名：<input type="text" name="name" size="6" placeholder="姓名" />
    密码：<input type="password" name="password" size="6" placeholder="密码" />
    验证：<input type="text" id="verify_text" name="verify_text" size="6" placeholder="验证码" />
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
    <div class="pure-g">
        <div class="pure-u-2-3">
            % if news:
                <div class="details">
                <p class="details_title">{{news.title}}</p>
                <p class="details_title">{{news.author}} {{news.release_date[:10]}}</p>
                    <div class="details_text">
                     {{!news.txt}}
                    </div>
                </div>
            %end
        </div>
        <div class="pure-u-1-3">
            <ul class="similar-news">
            <p style="text-align: center;">本类其他信息</p>
            %for new in more_news:
                <li>
                <a href="/news/{{str(new.id)}}" title="{{new.title}}">{{new.title}}</a>
                <span class="mydate">{{str(new.release_date)[:10]}}</span>
                </li>
            %end
            </ul>
        </div>
    </div>
