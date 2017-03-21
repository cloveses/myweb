% rebase('tpls/base.tpl')
<div class="pure-g">
<div class="pure-u-1-1" style="text-align: right;">
    {{info if info else ""}}
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

    %cols = 2
    %for i in range(0,2 * cols,cols):
    <div class="pure-g myclass">
        %for nav,news in newslist[i:i+cols]:
        <div class="pure-u-1-{{cols}}">
        <div class="mybox">
        <div>{{nav.name}}<a href="/{{nav.id}}" class="more">更多</a></div>
        %for new in news:
            <li>
                <a href="/news/{{str(new.id)}}" title="{{new.title}}">{{new.title}}</a>
                <span class="mydate">{{str(new.release_date)[:10]}}</span>
            </li>
        %end
        </div>
        </div>
        %end
    </div>
    %end
        <script type="text/javascript" src="/static/marquee.js"></script>
        <!--容器可以使用div，内容中使用ul li，那么框1就是div1，框2就是div2，需要两个div在一行，就需要设置div的float：left属性--> 
    <!--当然如果你对于css不是很了解，也可以使用table来实现，用td1和td2来实现。本人对table有种不喜，所以就通过div来做了--> 
        <div id="container" style="width:980px;height:160px;overflow:hidden;margin-left:5px;"> 
            <div id="longwidth" style="height:80px;width:1000%;"> 
                <div id="div1" class="kuang" style="float:left;height:160px;"> 
    <!--            <img src="./assets/img/98339876.jpg" width="240px" height="160px" /> 
                    <img src="./assets/img/98339876.jpg" width="240px" height="160px" /> 
                    <img src="./assets/img/98339876.jpg" width="240px" height="160px" /> 
                    <img src="./assets/img/98339876.jpg" width="240px" height="160px" /> 
                    <img src="./assets/img/98339876.jpg" width="240px" height="160px" /> 
                    <img src="./assets/img/98339876.jpg" width="240px" height="160px" /> 
                    <img src="./assets/img/98339876.jpg" width="240px" height="160px" />  -->
                    %for file_path in activeimgs:
                        <img src="{{file_path}}" width="240px" height="160px" />
                    %end
                </div> 
                <div id="div2" class="kuang" style="float:left;height:160px;margin-left:5px;"></div> 
            </div> 
        </div>

    %for i in range(2 * cols,len(newslist),cols):
    <div class="pure-g myclass">
        %for nav,news in newslist[i:i+cols]:
        <div class="pure-u-1-{{cols}}">
        <div class="mybox">
        <div>{{nav.name}}<a href="/{{nav.id}}" class="more">更多</a></div>
        %for new in news:
            <li>
                <a href="/news/{{str(new.id)}}" title="{{new.title}}">{{new.title}}</a>
                <span class="mydate">{{str(new.release_date)[:10]}}</span>
            </li>
        %end
        </div>
        </div>
        %end
        %if i >= 2 * cols:
            %break
        %end
    </div>
    %end