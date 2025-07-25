from Database import db, Category, User
from werkzeug.security import generate_password_hash

def insert_default_categories():
    default_categories = [
        {'id': 1, 'name': 'Building'},
        {'id': 2, 'name': 'Food'},
        {'id': 3, 'name': 'Other'}
    ]
    for category_data in default_categories:
        category = Category.query.filter_by(id=category_data['id']).first()
        if not category:
            new_category = Category(id=category_data['id'], name=category_data['name'])
            db.session.add(new_category)
    db.session.commit()

def insert_default_user():
    default_user_id = 'default_user'
    default_email = 'default@example.com'
    default_username = 'DefaultUser'
    default_password = 'changeme' 

    existing_user = User.query.filter_by(id=default_user_id).first()
    if not existing_user:
        new_user = User(
            id=default_user_id,
            username=default_username,
            email=default_email,
            password_hash=generate_password_hash(default_password)
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"默认用户 '{default_username}' 已插入。")
    else:
        print("默认用户已存在。")

if __name__ == "__main__":
    # 避免循环导入，延迟导入 application
    from application import application as app

    with app.app_context():
        insert_default_user()
        insert_default_categories()
