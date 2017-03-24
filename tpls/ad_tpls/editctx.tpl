% rebase('tpls/ad_tpls/base.tpl')
<script language="javascript" type="text/javascript" src="/ckeditor/ckeditor.js"></script>
% include('tpls/ad_tpls/aduserinfo.tpl',name=name,id=id)


%if name and power:
<div class="pure-g">
<div class="pure-u-1-1 headimg">
</div>
</div>
% include('tpls/ad_tpls/nav.tpl',user_type=user_type)
%end
%if name:
    <div>
    <form method="POST">
        <input type="text" name="title" size="97" value="{{news.title}}" placeholder="请输入标题" />
        <textarea name="txt">{{news.txt}}</textarea>
        <input type="submit" value="保存" />
    </form>
    </div>
    <script language="javascript" type="text/javascript">
    CKEDITOR.replace( 'txt', {
    "filebrowserImageUploadUrl":"/ckupload",
    // "language":"zh"
    }); 
    </script>
%end