# Auther: xyy
from database.config import db


############################################
# 数据库
############################################

# user ORM
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60))

    def __repr__(self):
        return '<User %r>' % self.username

    # 创建一条数据
    @staticmethod
    def create_one():
        admin = User(username="admin", password="CHANGE_ME_BEFORE_RUNNING")
        db.session.add(admin)
        db.session.commit()

    """
    辅助函数、装饰器
    登录检验（用户名、密码验证）
    """
    def valid_login(self, username, password):
        user = self.query.filter(db.and_(User.username == username, User.password == password)).first()
        if user:
            return user
        else:
            return False

    """
    用户id编号
    查询用户信息
    """
    def userinfo(self, userid):
        user = self.query.filter(db.and_(User.id == userid)).first()
        return user

    # 注册检验（用户名、邮箱验证）
    def valid_regist(self):
        user = self.query.filter(db.or_(User.username == self.username, User.email == self.email)).first()
        if user:
            return False
        else:
            return True

    def serialize(self):
        return {'username': self.username, 'password': self.password, 'id': self.id}

    # 用户信息注册
    def register(self, userinfo):
        db.session.add(userinfo)
        db.session.commit()


if __name__ == '__main__':
    user = User()
    flag = user.valid_login(username='admin', password='CHANGE_ME_BEFORE_RUNNING')
    print(flag)
