% rebase('tpls/ad_tpls/base.tpl')
<script type="text/javascript">
    $(function(){
        $(".editbutton").click(function(){
            idstr = $(this).attr('name');
            $('#'+idstr).show();
            $(".editbutton").hide()
        });
        $(".insertbutton").click(function(){
            idstr = $(this).attr('name');
            $('#'+idstr).show();
            $(".insertbutton").hide()
        });
    });
</script>
% include('tpls/ad_tpls/aduserinfo.tpl',name=name,id=id)
<div class="pure-g">
<div class="pure-u-1-1 headimg">
</div>
</div>

% include('tpls/ad_tpls/nav.tpl',user_type=user_type)
<div>
    <p>
        <a href="/lvlmgr">top</a>
        %for lid,lname in bread_nav:
        >><a href="/lvlmgr/{{lid}}">{{lname}}</a>
        %end
    </p>
    <table class="pure-table pure-table-horizontal">
        %for lvl in current_lvls:
        <tr>
            <td><a href="/lvlmgr/{{str(lvl.id)}}">{{lvl.name}}</a></td>
            <td><a href="/lvldel/{{'/'.join((str(lvl.id),parent_lid)) if parent_lid else str(lvl.id)}}" class="pure-button">删除</a></td>
            <td><button class="editbutton" name="{{str(lvl.id)}}" type="button" class="pure-button">修改</button></td>
            <td><span id="{{str(lvl.id)}}" style="display:none;">
            <form method="POST">
                <input type="text" size="8" name="name" value="{{lvl.name}}" placeholder="分类名称" />
                <input type="hidden" name="lid" value="{{str(lvl.id)}}" />
                <input type="hidden" name="action" value="edit" />
                <input type="submit" value="保存" />
            </form>
            </span>
            </td>

            <td><button class="insertbutton" name="insert{{str(lvl.id)}}" type="button" class="pure-button">插入</button></td>
            <td><span id="insert{{str(lvl.id)}}" style="display:none;">
            <form method="POST">
                <input type="text" size="8" name="name" placeholder="分类名称" />
                <input type="hidden" name="lid" value="{{str(lvl.id)}}" />
                <input type="hidden" name="action" value="insert" />
                <input type="submit" value="插入" />
            </form>
            </span>
            </td>
        </tr>
        %end
    </table>
</div>
<div>
<p>添加分类：</p>
<form action="" method="POST">
    <input type="text" name="name" placeholder="分类名称" required="required" />
    <input type="hidden" name="action" value="add" />
    <input type="hidden" name="parent_lid" value="{{parent_lid}}" />
    <input type="submit" value="添加" />
</form>
</div>