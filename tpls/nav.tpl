    <div class="pure-menu pure-menu-horizontal">
    <ul class="pure-menu-list">
    %if user_type == 100:
        <li class="pure-menu-item"v><a href="/usermgr" class="pure-menu-link">用户管理</a></li>
        <li class="pure-menu-item"><a href="/lvlmgr" class="pure-menu-link">分类管理</a></li>
    %else:
        <li class="pure-menu-item">用户管理</li>
        <li class="pure-menu-item">分类管理</li>
    %end
    <li class="pure-menu-item"><a href="/ctxmgr" class="pure-menu-link">内容管理</a></li>
    </ul>
    </div>