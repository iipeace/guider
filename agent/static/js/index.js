
Vue.use(new VueSocketIO({
    debug: true,
    connection: Vue.prototype.$serverAddr //'http://localhost:5000'
}))


var App = new Vue({
    el: "#app",
    sockets: {
        connect: function () {
            this.connectSocket();
        },
        server_response: function (msg) { // msg is json
            this.appendLog(msg.data + " timestamp: " + msg.timestamp + " length : " + msg.length_pipe);
            this.appendLog(msg.str_pipe);
        },
        request_stop_result : function (msg) {
            this.appendLog(msg);
        }
    },
    data: {
        clientMsg: "",
        log: "",
        targetTimestamp: "",
    },
    methods: {
        emitStart: function () {
            console.log("Start button Clicked!");
            var timestamp = + new Date();
            //this.$socket.emit('custom_connect', timestamp);
            this.$socket.emit('request_start', String(timestamp), { data: this.clientMsg });
        },
        emitStop: function () {
            console.log("Stop button Clicked!");
            //this.$socket.emit('custom_connect', timestamp);
            this.$socket.emit('request_stop', this.targetTimestamp);
        },
        appendLog: function (newLog) {
            this.log += newLog + "\n";
        },
        disconnectSocket: function() {
            this.$socket.disconnect();
        },
        connectSocket: function() {
            this.$socket.connect(); // if connection is not establised.
            this.appendLog("시작한다.  ");
        }
    },
    created: function () {
    }
})
