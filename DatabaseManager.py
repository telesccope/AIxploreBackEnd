import requests
from datetime import datetime
from application import application
from Database import *
import uuid


def update_user_password(user_id, new_password):
    """
    更新指定用户的密码。
    
    :param user_id: 用户的 ID
    :param new_password: 新密码
    :return: 成功返回 True，失败返回 False
    """
    try:
        # 查询用户
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            print(f"用户 ID {user_id} 不存在")
            return False
        
        # 设置新密码
        user.set_password(new_password)
        
        # 提交更改到数据库
        db.session.commit()
        
        print(f"用户 ID {user_id} 的密码已成功更新")
        return True
    except Exception as e:
        # 捕获异常并回滚事务
        db.session.rollback()
        print(f"更新密码时出错: {e}")
        return False
    
if __name__ == '__main__':
    from application import application
    with application.app_context():
        user_id = '2cc90736fd1c4a2d83e0a29c545f01b5'
        new_password = 'f86618661'
        update_user_password(user_id, new_password)