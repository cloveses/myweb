% rebase('tpls/ad_tpls/base.tpl')
<script language="javascript" type="text/javascript" src="/ckeditor/ckeditor.js"></script>
% include('tpls/ad_tpls/aduserinfo.tpl',name=name,id=id)


%if name and power:
    % include('tpls/ad_tpls/nav.tpl',user_type=user_type)
    <div>
        <p>所有分类：</p>
        %for p in power:
        <a href="/ctxmgr/{{str(p.id)}}" class="pure-button ctxmgr-a">{{p.name}}</a>
        %end
        <p>
        %if lname:
        当前分类：{{lname}}
        %end
        %for lid,lname in bread_nav:
        >><a href="/ctxmgr/{{lid}}" class="pure-button ctxmgr-a">{{lname}}</a>
        %end
        %for nv in next_lvls:
        <a href="/ctxmgr/{{str(nv.id)}}" class="pure-button ctxmgr-a">{{nv.name}}</a>
        %end
        </p>
    </div>
    <div>
        <table class="pure-table">
        %if news:
            <thead>
                <th>标题</th>
                <th>内容</th>
                <th>日期</th>
                <th>审核</th>
                <th>删除</th>
                <th>编辑</th>
            </thead>
        %end
            %for new in news:
            <tr>
                <td>{{new.title}}</td>
                <td>{{new.txt[:10]}}</td>
                <td>{{str(new.release_date)[:19]}}</td>
                <td><input type="checkbox" {{"checked" if new.is_released else ""}}  form="save_check" name="{{str(new.id)}}-rels" value="{{str(new.id)}}" />审核通过</td>
                <td><a href="/delctx/{{str(new.id)}}/{{lid}}{{'/'+str(page) if page else ''}}" class="ctxmgr-a">删除</a></td>
                <td><a href="/editctx/{{lid}}/{{str(new.id)}}{{'/'+str(page) if page else ''}}" class="ctxmgr-a">修改</a></td>
            </tr>
            %end
        </table>
        <p>
            %for i in pages:
            <a href="/ctxmgr/{{lid}}/{{i}}">第{{i+1}}页　</a>
            %end
        </p>
        %if news:
        <form id="save_check" method="POST">
            <input type="hidden" name="lid" value="{{lid}}" />
            <input type="hidden" name="action" value="release" />
            <input type="submit" value="保存所有审核" />
        </form>
        %end
    </div>
%if lname:
    <div>
    <p>为当前分类添加内容：</p>
    <form method="POST">
        <input type="text" name="title" size="97" placeholder="请输入标题" />
        <input type="hidden" name="uid" value="{{id}}" />
        <br/>
        <textarea name="txt" cols="73" rows="10" placeholder="在此输入内容"></textarea>
        <input type="hidden" name="lid" value="{{lid}}" />
        <input type="hidden" name="action" value="add">
        <br/>
        <input type="submit" value="保存" />
    </form>
    </div>
    <script language="javascript" type="text/javascript">
    CKEDITOR.replace( 'txt', {
    "filebrowserImageUploadUrl":"/ckupload"
    }); 
    </script>
%else:
    <h2>请选择分类添加内容！</h2>
%end
%end