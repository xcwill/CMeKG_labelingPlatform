from _init_ import db


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    role = db.Column(db.String(32), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


class Code(db.Model):
    __tablename__ = 'codes'
    email = db.Column(db.String(32), unique=True, nullable=False, primary_key=True)
    code = db.Column(db.String(32), nullable=False)
    time = db.Column(db.String(32), nullable=False)


class File(db.Model):
    __tablename__ = 'files'
    name = db.Column(db.String(32), unique=True, nullable=False, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    count = db.Column(db.String(32), nullable=False)
    time = db.Column(db.String(32), nullable=False)
    user = db.Column(db.String(32), nullable=False)
    words = db.Column(db.String(32), nullable=False)

class Task(db.Model):
    __tablename__ = 'tasks'
    name = db.Column(db.String(32), unique=True, nullable=False, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    count = db.Column(db.String(32), nullable=False)
    time = db.Column(db.String(32), nullable=False)
    user = db.Column(db.String(32), nullable=False)
    words = db.Column(db.String(32), nullable=False)

class Group(db.Model):
    __tablename__ = 'groups'
    group_name = db.Column(db.String(32), unique=True, nullable=False, primary_key=True)

class Task_User(db.Model):
    __tablename__ = 'task_user'
    name = db.Column(db.String(32), nullable=False, primary_key=True)
    username = db.Column(db.String(32), nullable=False, primary_key=True)

class Task_Group(db.Model):
    __tablename__ = 'task_group'
    name = db.Column(db.String(32), nullable=False, primary_key=True)
    group_name = db.Column(db.String(32), nullable=False, primary_key=True)

class Group_user(db.Model):
    __tablename__ = 'group_user'
    group_name = db.Column(db.String(32), nullable=False, primary_key=True)
    username = db.Column(db.String(32), nullable=False, primary_key=True)

class Task_File(db.Model):
    __tablename__ = 'task_file'
    task_name = db.Column(db.String(32), nullable=False, primary_key=True)
    file_name = db.Column(db.String(32), nullable=False, primary_key=True)


if __name__ == '__main__':
    db.create_all()
