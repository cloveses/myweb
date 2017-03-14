    <div class="pure-menu pure-menu-horizontal">
    <ul class="pure-menu-list">
        <li class="pure-menu-item"><a href="/" class="pure-menu-link">首页</a></li>
        %for nav in navs:
        <li class="pure-menu-item"><a href="/{{str(nav.id)}}" class="pure-menu-link">{{nav.name}}</a></li>
        %end
    </ul>
    </div>