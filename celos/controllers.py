import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.websocket
import os.path
import uuid

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

from .models import Entry, Host
import settings as SETTINGS

log = SETTINGS.LOG

WEBSOCKET_CONNECTIONS = []

class IndexHandler(tornado.web.RequestHandler):
    def get(self):

        entries = Entry.objects.order_by('-timestamp')
        e = Entry.objects.filter(timestamp__gt=entries[10].timestamp)
        log.debug(e)
        self.render('index.html', **{
            'entries': entries,
        })

class EntryCreateHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('log_dummy.html')

    def post(self):
        log.debug(self.get_argument('msg', ''))
        entry = Entry(
            host = Host(ip=self.request.remote_ip, user_agent=self.request.headers['User-Agent']),
            lvl = self.get_argument('lvl', 0),
            msg = self.get_argument('msg', ''),
            stack_trace = self.get_argument('stack_trace', ''),
        )
        entry.save() # Entry(...).save() introduces a racecondition - this is the workaround
        log.debug(entry)
        html = tornado.escape.to_basestring(self.render_string('entry.html', entry=entry))

        #self.write(html)

        for con in WEBSOCKET_CONNECTIONS:
            con.write_message(html)

        self.render('log_dummy.html')

class SubscriptionSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        log.debug('Websocket opened')
        WEBSOCKET_CONNECTIONS.append(self)

    def on_close(self):
        log.debug('Websocket closed')
        WEBSOCKET_CONNECTIONS.remove(self)

    def on_message(self, msg):
        self.write_message('Echo: '+msg)

    def check_origin(self, origin):
        return True


"""
class EntrySubscriptionHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        cursor = self.get_argument('cursor', None)
        if cursor is None:
            if Entry.objects.
        new_entries = Entry.objects.filter(timestamp__gt=cursor.timestamp)
        #cursor = self.get_argument('cursor', None)
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        #self.future = global_message_buffer.wait_for_messages(cursor=cursor)
        #messages = yield self.future
        #if self.request.connection.stream.closed():
        #    return
        log.debug()
        self.write(dict(entries=new_entries))

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.future)

"""

'''
class Host(EmbeddedDocument):
    ip = StringField()
    user_agent = StringField()
    user_agent_hashed = StringField()



class Entry(Document):
    host = EmbeddedDocumentField('Host')
    lvl = IntField()
    msg = StringField()
    timestamp = DateTimeField(default=datetime.datetime.now)
'''

class MessageNewHandler(object):
    @tornado.web.authenticated
    def post(self):
        message = {
            'id': str(uuid.uuid4()),
            'from': self.current_user['first_name'],
            'body': self.get_argument('body'),
            'user_agent': self.get_argument('user_agent'),
        }
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        message['html'] = tornado.escape.to_basestring(
            self.render_string('message.html', message=message))
        if self.get_argument('next', None):
            self.redirect(self.get_argument('next'))
        else:
            self.write(message)
        global_message_buffer.new_messages([message])


class MessageUpdatesHandler(object):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        cursor = self.get_argument('cursor', None)
        print('cursor')
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        self.future = global_message_buffer.wait_for_messages(cursor=cursor)
        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.future)