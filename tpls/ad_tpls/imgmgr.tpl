% rebase('tpls/ad_tpls/base.tpl')
<script language="javascript" type="text/javascript" src="/ckeditor/ckeditor.js"></script>
% include('tpls/ad_tpls/aduserinfo.tpl',name=name,id=id)


%if name:
    <div class="pure-g">
    <div class="pure-u-1-1 headimg">
    </div>
    </div>

    % include('tpls/ad_tpls/nav.tpl',user_type=user_type)
    <div style="height: 400px;margin-top: 30px;">
        <p>请选择要上传的图片：</p>
        <form method="POST"  enctype="multipart/form-data" class="pure-form pure-form-stacked pure-form-aligned">
            <label for="titlename">图片标题</label>
            <input type="text" name="titlename" placeholder="图片标题" />
            <label for="upload">选择图片</label>
            <input type="file" name="upload" />
            <input type="submit" value="上传" />
        </form>
    </div>
%end