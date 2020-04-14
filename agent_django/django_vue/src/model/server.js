export class Server {
  targetAddr = "";
  status = Status.STOP;
  healthCheckInterval = null;
  interval = 10000;
  retryCount = 0;
  requestId = "";
  sockets = null;
  socket = null;

  constructor(targetAddr) {
    this.targetAddr = targetAddr;
  }

  hasTargetAddr() {
    return !!this.targetAddr;
  }

  healthCheck(sockets, socket) {
    if (this.healthCheckInterval) {
      return;
    }
    this.sockets = sockets;
    this.socket = socket;
    this.status = Status.START;
    this.healthCheckInterval = setInterval(() => {
      this.sendCommand();
    }, this.interval);
  }

  sendCommand() {
    if (!this.hasTargetAddr()) {
      alert("please set target address");
      return false;
    }
    if (this.requestId !== "") {
      return;
    }
    this.requestId = `${this.targetAddr}-${new Date().getTime()}`;

    this.sockets.subscribe(this.requestId, data => {
      if (data.result === 0) {
        this.data = data.data;
        this.resetRetryCount();
      } else if (data.result < 0) {
        alert(data.errorMsg);
        this.retry();
      }
    });

    this.sockets.subscribe(`${this.requestId}_stop`, data => {
      if (data.result === 0) {
        this.sockets.unsubscribe(this.requestId);
        this.sockets.unsubscribe(`${this.requestId}_stop`);
        this.requestId = "";
      } else if (data.result < 0) {
        alert(data.errorMsg);
      }
    });
    this.socket.emit("health_check", this.targetAddr, this.requestId);
  }

  retry() {
    this.retryCount++;
    this.status = Status.SUSPEND;
    if (this.retryCount > 5) {
      this.clear();
    }
  }

  resetRetryCount() {
    this.retryCount = 0;
    if (Status.SUSPEND) {
      this.status = Status.START;
    }
  }

  clear() {
    if (this.requestId) {
      this.sockets.unsubscribe(this.requestId);
      this.sockets.unsubscribe(`${this.requestId}_stop`);
      this.socket.emit("stop_command_run", this.requestId);
    }
    this.clearInterval();
    this.resetRetryCount();
    this.status = Status.STOP;
  }

  clearInterval() {
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }
  }
}

export const Status = {
  START: 0,
  RUNNING: 1,
  SUSPEND: 2,
  STOP: 9
};
