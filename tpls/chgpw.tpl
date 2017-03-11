% rebase('tpls/base.tpl')
<div>
% include('tpls/userinfo.tpl',name=name,id=id)

% include('tpls/nav.tpl',user_type=user_type)
<div>
<form action="" method="POST">
    <p>旧密码：　<input type="password" name="opassword" required="required" /></p>
    <p>新密码：　<input type="password" name="npassword"  required="required" /></p>
    <p>验证密码：<input type="password" name="kpassword" required="required" /></p>
    <p><input type="submit" value="修改密码" /></p>
</form>
</div>