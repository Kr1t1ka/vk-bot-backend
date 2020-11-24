from main import db
import datetime


class Inheritances(db.Model):
    __tablename__ = "inheritances"

    id_inher = db.Column(db.Integer, primary_key=True)
    menu_id_ancestor = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menu_id_descendant = db.Column(db.Integer, db.ForeignKey('menu.id'))
    reversible = db.Column(db.Boolean, nullable=False, default=True)
    added = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author_id = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Inheritances %r>' % self.id_inher


class Menu(db.Model):
    __tablename__ = "menu"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), default='default_name')
    text = db.Column(db.String(10000), default='default_text')
    added = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author_id = db.Column(db.Integer, nullable=False, default=0)
    tags = db.Column(db.String(5000), default='нет тегов')
    inheritances = db.relationship('Inheritances',
                                   primaryjoin="or_(Menu.id==Inheritances.menu_id_descendant, Menu.id==Inheritances.menu_id_ancestor)",
                                   lazy='dynamic')
    attachment = db.relationship('Attachment',
                                 primaryjoin="Menu.id==Attachment.menu_id",
                                 lazy='dynamic')

    def __repr__(self):
        return '<Menu %r>' % self.id


class Attachment(db.Model):
    __tablename__ = 'attachment'

    id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), unique=True)
    attachment_active = db.Column(db.Boolean, default=True)
    vk_active = db.Column(db.Boolean, nullable=False, default=True)
    telegram_active = db.Column(db.Boolean, nullable=False, default=True)
    vk_attachment = db.Column(db.String(120), default='photo-128637216_456239172')
    telegram_attachment = db.Column(db.String(120), default='default_name')

    def __repr__(self):
        return '<Attachment %r>' % self.id


class Replace(db.Model):
    __tablename__ = "replace"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.String(120), default='(перменная не определена)')
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    active = db.Column(db.Boolean, nullable=False, default=True)
    author_id = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Replace %r>' % self.id


# class Users(db.Model):
#     __tablename__ = "users"
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(240), unique=True, nullable=False)
#     poll_step = db.Column(db.Integer, default=0)
#     poll = db.Column(db.Integer, default=0)
#
#     def __repr__(self):
#         return '<Users %r>' % self.id
#
#
# class Poll(db.Model):
#     __tablename__ = 'poll'
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(240), default='Poll name')
#     step_limit = db.Column(db.Integer, default=10)
#
#     def __repr__(self):
#         return '<Poll %r>' % self.id
#
#
# class PollStep(db.Model):
#     __tablename__ = 'poll_step'
#
#     id = db.Column(db.Model, primary_key=True)
#     question = db.Column(db.String(1000), default='вопрос в опросе')
#     poll_id = db.Column(db.Integer, default=0)
#
#     def __repr__(self):
#         return '<PollStep %r>' % self.id
#
#
# class User







