% rebase('tpls/base.tpl')
<script language="javascript" type="text/javascript" src="/ckeditor/ckeditor.js"></script>
% include('tpls/userinfo.tpl',name=name,id=id)


%if name:
    % include('tpls/nav.tpl',user_type=user_type)
    <div style="height: 400px;margin-top: 30px;">
        <p>请选择要上传的图片：</p>
        <form method="POST"  enctype="multipart/form-data">
            <input type="file" name="upload" />
            <input type="submit" value="上传" />
        </form>
    </div>
%end