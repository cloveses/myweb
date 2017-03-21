    <div class="pure-menu pure-menu-horizontal">
    <ul class="pure-menu-list">
    %if user_type == 100:
        <li class="pure-menu-item"><a href="/usermgr" class="pure-menu-link">用户管理</a></li>
        <li class="pure-menu-item"><a href="/lvlmgr" class="pure-menu-link">分类管理</a></li>
    %else:
        <li class="pure-menu-item"><a href="#" class="pure-menu-link">用户管理</a></li>
        <li class="pure-menu-item"><a href="#" class="pure-menu-link">分类管理</a></li>
    %end
        <li class="pure-menu-item"><a href="/ctxmgr" class="pure-menu-link">内容管理</a></li>
        <li class="pure-menu-item"><a href="/imgmgr" class="pure-menu-link">动态图片</a></li>
    </ul>
    </div>