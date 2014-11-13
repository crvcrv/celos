import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid

from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line

from mongoengine import connect


import celos.controllers
#from celos.controllers import IndexHandler, EntryCreateHandler

import settings as SETTINGS

log = SETTINGS.LOG


"""
class MessageNewHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "from": self.current_user["first_name"],
            "body": self.get_argument("body"),
        }
        # to_basestring is necessary for Python 3's json encoder,
        # which doesn't accept byte strings.
        message["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=message))
        if self.get_argument("next", None):
            self.redirect(self.get_argument("next"))
        else:
            self.write(message)
        global_message_buffer.new_messages([message])


class MessageUpdatesHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        cursor = self.get_argument("cursor", None)
        # Save the future returned by wait_for_messages so we can cancel
        # it in wait_for_messages
        self.future = global_message_buffer.wait_for_messages(cursor=cursor)
        messages = yield self.future
        if self.request.connection.stream.closed():
            return
        self.write(dict(messages=messages))

    def on_connection_close(self):
        global_message_buffer.cancel_wait(self.future)


class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    @gen.coroutine
    def get(self):
        if self.get_argument("openid.mode", None):
            user = yield self.get_authenticated_user()
            self.set_secure_cookie("chatdemo_user",
                                   tornado.escape.json_encode(user))
            self.redirect("/")
            return
        self.authenticate_redirect(ax_attrs=["name"])


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("chatdemo_user")
        self.write("You are now logged out")
"""

if __name__ == '__main__':
    if SETTINGS.MONGO['USERNAME']:
        connect(
            SETTINGS.MONGO['NAME'], 
            username = SETTINGS.MONGO['USERNAME'], 
            password = SETTINGS.MONGO['PASSWORD'],
            host = SETTINGS.MONGO['HOST'],
            port = SETTINGS.MONGO['PORT'],
        )
    else:
        connect(
            SETTINGS.MONGO['NAME'],
            host = SETTINGS.MONGO['HOST'],
            port = SETTINGS.MONGO['PORT'],
        )

    app = tornado.web.Application(
        (
            (r'/', celos.controllers.IndexHandler),
            (r'/entry/new', celos.controllers.EntryCreateHandler),
            (r'/entry/notifier', celos.controllers.SubscriptionSocketHandler)
            #(r'/entry/subscribe', EntrySubscriptionHandler),
        ),
        cookie_secret = SETTINGS.SECRET_KEY,
        login_url = SETTINGS.LOGIN_URL,
        template_path = SETTINGS.TEMPLATE_PATH,
        static_path = SETTINGS.STATIC_PATH,
        #xsrf_cookies = True,
        debug = SETTINGS.DEBUG,

    )

    app.listen(SETTINGS.PORT)

    tornado.ioloop.IOLoop.instance().start()
