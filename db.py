from models import User,Code,File,Task,Task_User,Task_File,Group,Task_Group,Group_user
from _init_ import db


class DB:
    @staticmethod
    def add_user(username, email, password, role):
        user = User(username=username, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def query_all():
        return User.query.all()

    @staticmethod
    def query_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def query_by_role(role):
        return User.query.filter_by(role=role)

    @staticmethod
    def query_by_email(email):
        return User.query.filter_by(email=email).first()

    def check_login(self, username, email, password):
        if self.query_by_username(username) is not None or self.query_by_email(email) is not None:
            if self.query_by_username(username) is not None and self.query_by_username(username).password == password:
                return 1
            elif self.query_by_email(email) is not None and self.query_by_email(email).password == password:
                return 1
            else:
                return 0
        else:
            return -1

    def new_password(self, username, email, password):
        if self.query_by_username(username) is not None or self.query_by_email(email) is not None:
            if self.query_by_username(username) is not None:
                u = self.query_by_username(username)
                u.password = password
                db.session.add(u)
                db.session.commit()
            if self.query_by_email(email) is not None:
                u = self.query_by_email(email)
                u.password = password
                db.session.add(u)
                db.session.commit()

    def add_code(self, email, code, time):
        if self.query_code_by_email(email) is not None:
            c = self.query_code_by_email(email)
            c.code = code
            c.time = time
            db.session.add(c)
            db.session.commit()
        else:
            code = Code(email=email, code=code, time=time)
            db.session.add(code)
            db.session.commit()

    @staticmethod
    def query_code_by_email(email):
        return Code.query.filter_by(email=email).first()

    @staticmethod
    def add_file(name, type, count, time, user, words):
        file = File(name=name, type=type, count=count, time=time, user=user, words=words)
        db.session.add(file)
        db.session.commit()

    @staticmethod
    def query_file_by_name(name):
        return File.query.filter_by(name=name).first()

    @staticmethod
    def query_all_files():
        return File.query.all()

    @staticmethod
    def add_task_user(name, username):
        t_u = Task_User(name=name, username=username)
        db.session.add(t_u)
        db.session.commit()

    @staticmethod
    def query_all_tasks():
        return Task.query.all()

    @staticmethod
    def query_task_by_user(username):
        return Task_User.query.filter_by(username=username)

    @staticmethod
    def query_task_by_name(name):
        return Task.query.filter_by(name=name).first()

    @staticmethod
    def add_task(name, ty, count, time, user, words):
        t = Task(name=name, type=ty, count=count, time=time, user=user, words=words)
        db.session.add(t)
        db.session.commit()

    @staticmethod
    def query_task_exist(name):
        return Task.query.filter_by(name=name).first()

    @staticmethod
    def query_task_user_exist(name, username):
        return Task_User.query.filter_by(name=name, username=username).first()

    @staticmethod
    def add_task_file(task_name, file_name):
        t_f = Task_File(task_name=task_name, file_name=file_name)
        db.session.add(t_f)
        db.session.commit()

    @staticmethod
    def query_task_file_exist(task_name, file_name):
        return Task_File.query.filter_by(task_name=task_name, file_name=file_name).first()

    @staticmethod
    def query_task_file_exist_by_file_name(file_name):
        return Task_File.query.filter_by(file_name=file_name)

    @staticmethod
    def query_task_file_by_task(task_name):
        return Task_File.query.filter_by(task_name=task_name)

    @staticmethod
    def del_task_by_name(name):
        t = Task.query.filter_by(name=name).first()
        db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_task_user_by_name(name):
        ta = Task_User.query.filter_by(name=name).all()
        for t in ta:
            db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_task_user_by_name_username(name, username):
        t = Task_User.query.filter_by(name=name, username=username).first()
        db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_file_by_file_name(name):
        t = File.query.filter_by(name=name).first()
        db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_task_file_by_task_name(name):
        ta = Task_File.query.filter_by(task_name=name).all()
        for t in ta:
            db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_task_file_by_file_name(file_name):
        ta = Task_File.query.filter_by(file_name=file_name).all()
        for t in ta:
            db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_task_file_by_task_name_file_name(task_name, file_name):
        t = Task_File.query.filter_by(task_name=task_name, file_name=file_name).first()
        db.session.delete(t)
        db.session.commit()

    @staticmethod
    def query_task_user_by_name(name):
        return Task_User.query.filter_by(name=name)

    @staticmethod
    def upd_task_name(name, new_name):
        t = Task.query.filter_by(name=name).first()
        t.name = new_name
        db.session.commit()

    @staticmethod
    def upd_file_name(name, new_name):
        t = File.query.filter_by(name=name).first()
        t.name = new_name
        db.session.commit()

    @staticmethod
    def upd_task_file_by_file_name(file_name, new_name):
        fs = Task_File.query.filter_by(file_name=file_name)
        for f in fs:
            f.file_name = new_name
        db.session.commit()

    @staticmethod
    def query_all_groups():
        return Group.query.all()

    @staticmethod
    def add_new_group(group_name):
        g = Group(group_name=group_name)
        db.session.add(g)
        db.session.commit()

    @staticmethod
    def del_group_by_group_name(group_name):
        g = Group.query.filter_by(group_name=group_name).first()
        db.session.delete(g)
        db.session.commit()

    @staticmethod
    def query_group_exist(group_name):
        return Group.query.filter_by(group_name=group_name).first()

    @staticmethod
    def query_task_group_by_task_name(name):
        return Task_Group.query.filter_by(name=name)

    @staticmethod
    def query_task_group_by_group_name(group_name):
        return Task_Group.query.filter_by(group_name=group_name)

    @staticmethod
    def query_task_group_exist(task_name, group_name):
        return Task_Group.query.filter_by(name=task_name, group_name=group_name).first()

    @staticmethod
    def query_task_group_exist_by_group_name(group_name):
        return Task_Group.query.filter_by(group_name=group_name)

    @staticmethod
    def add_task_group(name, group_name):
        t_g = Task_Group(name=name, group_name=group_name)
        db.session.add(t_g)
        db.session.commit()

    @staticmethod
    def del_task_group_by_task_name(name):
        ta = Task_Group.query.filter_by(name=name).all()
        for t in ta:
            db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_task_group_by_group_name(group_name):
        ta = Task_Group.query.filter_by(group_name=group_name).all()
        for t in ta:
            db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_task_group_by_task_name_group_name(task_name, group_name):
        t = Task_Group.query.filter_by(name=task_name, group_name=group_name).first()
        db.session.delete(t)
        db.session.commit()

    @staticmethod
    def query_group_user_by_group_name(group_name):
        return Group_user.query.filter_by(group_name=group_name)

    @staticmethod
    def query_group_user_by_username(username):
        return Group_user.query.filter_by(username=username)

    @staticmethod
    def query_group_user_exist(group_name, username):
        return Group_user.query.filter_by(group_name=group_name, username=username).first()

    @staticmethod
    def add_group_user(group_name, username):
        g_u = Group_user(group_name=group_name, username=username)
        db.session.add(g_u)
        db.session.commit()

    @staticmethod
    def del_group_user_by_group_name(group_name):
        ta = Group_user.query.filter_by(group_name=group_name).all()
        for t in ta:
            db.session.delete(t)
        db.session.commit()

    @staticmethod
    def del_group_user_by_group_name_username(group_name, username):
        t = Group_user.query.filter_by(group_name=group_name, username=username).first()
        db.session.delete(t)
        db.session.commit()

    @staticmethod
    def upd_group_name(group_name, new_name):
        t = Group.query.filter_by(group_name=group_name).first()
        t.group_name = new_name
        db.session.commit()

    @staticmethod
    def upd_task_group_name(group_name, new_name):
        ts = Task_Group.query.filter_by(group_name=group_name)
        for t in ts:
            t.group_name = new_name
        db.session.commit()


