import datetime
import hashlib

from mongoengine import *

class Host(EmbeddedDocument):
    ip = StringField()
    user_agent = StringField()
    user_agent_hashed = StringField()

    def colorful_hash():
        doc = "The colorful_hash property."
        def fget(self):
            r = self.user_agent_hashed[:2]
            g = self.user_agent_hashed[19:21]
            b = self.user_agent_hashed[-2:]
            return ''.join([r,g,b])
        return locals()
    colorful_hash = property(**colorful_hash())

    def gravatar(self):
        s = '{ip}:{user_agent}'.format(ip=self.ip, user_agent=self.user_agent)
        user_agent_md5 = hashlib.md5(s.encode()).hexdigest()
        return 'http://www.gravatar.com/avatar/{0}?d=retro&s=50'.format(user_agent_md5)



class Entry(Document):
    host = EmbeddedDocumentField('Host')
    lvl = IntField()
    msg = StringField()
    stack_trace = StringField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.host.user_agent_hashed = hashlib.sha1(self.host.user_agent.encode()).hexdigest()

        super(Entry, self).save(*args, **kwargs)
