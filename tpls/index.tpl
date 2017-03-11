% rebase('tpls/base.tpl')

% include('tpls/userinfo.tpl',name=name,id=id)

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