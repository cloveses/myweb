% rebase('tpls/base.tpl')
<script type="text/javascript">
    $(function(){
        $(".editbutton").click(function(){
            idstr = $(this).attr('name');
            $('#'+idstr).show();
            $(".editbutton").hide()
        });
    });
</script>
% include('tpls/userinfo.tpl',name=name,id=id)

% include('tpls/nav.tpl',user_type=user_type)
<div>
    <table style="margin-top: 20px;" class="pure-table">
        %for u,p in zip(users,powers):
        <tr>
            <td><input type="checkbox" name="{{str(u.id)}}-chkbox" value="{{str(u.id)}}" form="save_power" /></td>
            <td>{{u.name}}</td>
            <td>{{p}}</td>
            <td><a href="/userdel/{{str(u.id)}}">删除</a></td>
            <td><button class="editbutton" name="{{str(u.id)}}" type="button">修改</button></td>
            <td><span id="{{str(u.id)}}" style="display:none;">
            <form method="POST">
                <input type="text" size="8" name="name" value="{{u.name}}" placeholder="姓名" />
                <input type="password" size="8" name="password" value="" placeholder="密码" />
                <input type="hidden" name="uid" value="{{str(u.id)}}" />
                <input type="hidden" name="action" value="edit" />
                <input type="submit" value="保存" />
            </form>
            </span></td>
        </tr>
        %end
    </table>
    <table style="margin-top: 20px;" class="pure-table">
        %for lvl in lvls:
        <tr>
            <td><input type="checkbox" name="{{str(lvl.id)}}-vchkbox" value="{{str(lvl.id)}}"  form="save_power" /></td>
            %for i in range(lvl.c):
                <td></td>
            %end
            <td>{{lvl.name}}</td>
        </tr>
        %end
    </table>
    <form method="POST" id="save_power">
    <input type="hidden" name="action" value="power" />
    <input type="submit" value="保存权限" />
    </form>
</div>
<div style="margin-top: 20px;">
<form action="" method="POST">
    <label for="name">用户名：</label>
    <input type="text" name="name" placeholder="用户名" required="required" />
    <label for="password">密码：</label>
    <input type="password" name="password" placeholder="密码" required="required" />
    <input type="hidden" name="action" value="add" />
    <input type="submit" value="添加" />
</form>
</div>