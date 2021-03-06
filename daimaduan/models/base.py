# coding: utf-8
import hashlib
import time

from daimaduan.models.bookmark import Bookmark
from daimaduan.models.message import Message
from daimaduan.utils.pagination import get_page

from daimaduan.bootstrap import db
from daimaduan.models import BaseDocument
from daimaduan.models.user_oauth import UserOauth


class User(BaseDocument):
    username = db.StringField(required=True)
    email = db.StringField(required=True)
    password = db.StringField()
    salt = db.StringField()
    is_email_confirmed = db.BooleanField(default=False)
    email_confirmed_on = db.DateTimeField(default=None)
    number = db.IntField(default=0, unique=True)
    description = db.StringField(default=u"这个家伙很懒, TA什么都没写...")

    oauths = db.ListField(db.ReferenceField(UserOauth))

    likes = db.ListField(db.ReferenceField('Paste'))
    followings = db.ListField(db.ReferenceField('User'))

    @property
    def pastes(self):
        return Paste.objects(user=self)

    @property
    def pastes_count(self):
        return len(self.pastes)

    @property
    def comments_count(self):
        return len(Comment.objects(user=self))

    @property
    def private_pastes_count(self):
        return len(self.pastes(is_private=True))

    @property
    def public_pastes_count(self):
        return len(self.pastes) - len(self.pastes(is_private=True))

    @property
    def public_bookmarks(self):
        return Bookmark.objects(user=self, is_private=False)

    @property
    def public_bookmarks_count(self):
        return Bookmark.objects(user=self, is_private=False).count()

    @property
    def unread_messages_count(self):
        return Message.objects(user=self, is_read=False).count()

    def save(self, *args, **kwargs):
        if not self.salt:
            self.salt = hashlib.sha1(str(time.time())).hexdigest()
            self.password = self.generate_password(self.password)
            number = User.objects().count() + 1
            while(User.objects(number=number).first()):
                number += 1
            self.number = number
        super(User, self).save(*args, **kwargs)

    def owns_record(self, record):
        return record.user == self

    def generate_password(self, string):
        return hashlib.sha1('%s%s' % (string, self.salt)).hexdigest()

    def check_login(self, password):
        return self.generate_password(password) == self.password

    @classmethod
    def find_by_oauth(cls, provider, openid):
        """Find user that has oauth info with given provider and openid"""
        oauth = UserOauth.objects(provider=provider, openid=openid).first()

        if oauth and oauth.user:
            return oauth.user

    def is_following(self, user):
        return user in self.followings

    @property
    def followers(self):
        return User.objects(followings=self)


class Code(db.EmbeddedDocument):
    title = db.StringField()
    syntax = db.ReferenceField('Syntax')
    content = db.StringField(required=True)

    def content_head(self, n=10):
        lines = self.content.splitlines()[:n]
        return '\n'.join(lines)

    @property
    def highlight_content(self):
        return self.content


class Paste(BaseDocument):
    user = db.ReferenceField(User)

    title = db.StringField()
    hash_id = db.StringField(unique=True)
    is_private = db.BooleanField(default=False)
    codes = db.ListField(db.EmbeddedDocumentField(Code))
    tags = db.ListField(db.ReferenceField('Tag'))

    views = db.IntField(default=0)

    @property
    def comments(self):
        page = get_page()
        return Comment.objects(paste=self).order_by('-created_at').paginate(page=page, per_page=20)

    @property
    def comments_count(self):
        return Comment.objects(paste=self).count()

    def save(self, *args, **kwargs):
        self.create_hash_id(self.user.salt, 'paste')
        if not self.title:
            self.title = u'代码集合: %s' % self.hash_id
        super(Paste, self).save(*args, **kwargs)

    def increase_views(self):
        self.views = self.views + 1
        self.save()

    def is_user_owned(self, user):
        return self.user == user

    @property
    def likes_count(self):
        return User.objects(likes=self).count()


class Comment(BaseDocument):
    hash_id = db.StringField(unique=True)
    user = db.ReferenceField(User)
    paste = db.ReferenceField(Paste)
    content = db.StringField()

    def save(self, *args, **kwargs):
        self.create_hash_id(self.user.salt, 'comment')
        super(Comment, self).save(*args, **kwargs)

    def is_user_owned(self, user):
        return self.user == user
