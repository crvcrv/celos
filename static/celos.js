var HOST = "172.30.4.121:8000";

$(document).ready(function () {
    var ws = new WebSocket("ws://"+HOST+"/entry/notifier");
    ws.onopen = function() {
        ws.send("Hello, world");
    };
    ws.onmessage = function(msg) {
        $('#logs').prepend(msg.data)
    };
});

var Log = Error;
Log.prototype.debug = function () {
    var args = Array.prototype.slice.call(arguments, 0);
    var stack = this.lineNumber ? 'line: '  + this.lineNumber : 'stack: ' + this.stack;

    Celos.logit.apply({}, [args.join(), this.stack, 0]);
    console.log.apply(console, args.concat([stack]));
};


var Celos = {

    post: function(data){
        console.log(data)
        $.ajax({
            url: "/entry/new", 
            type: "POST", 
            dataType: "text",
            data: $.param(data), 
            success: Celos.onSuccess,
            error: Celos.onError
        });
    },
    logit: function(msg, stack, lvl){
        Celos.post({
            msg: msg,
            stack_trace: stack,
            lvl: lvl,
        });
    },
    debug: function(msg, stack){
        m = {
            lvl: 0,
            msg: msg,
            stack_trace: stack,
        }
        Celos.post(m)
    },
    info: function(msg){
        m = {
            lvl: 1,
            msg: msg,
            stack_trace: stack,
        }
        Celos.post(m)
    },
    warn: function(msg){
        m = {
            lvl: 2,
            msg: msg,
            stack_trace: stack,
        }
        Celos.post(m)
    },
    error: function(msg){
        m = {
            lvl: 3,
            msg: msg,
            stack_trace: stack,
        }
        Celos.post(m)
    },
    critical: function(msg){
        m = {
            lvl: 4,
            msg: msg,
        }
        Celos.post(m)
    },

    onSuccess: function(){
        return true;
    },
    onError: function(){
        return true;
    }


}
/*

window.addEventListener("error", function(e){
    Logger.error(e.message)
    console.log(e.lineno)
})

var Log = Error;
Log.prototype.write = function () {
    var args = Array.prototype.slice.call(arguments, 0),
        suffix = this.lineNumber ? 'line: '  + this.lineNumber : 'stack: ' + this.stack;

    console.log.apply(console, args.concat([suffix]));
};
*/