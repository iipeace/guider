export default class GuiderDataSet {
  timestamp = 0;
  inbound = [];
  outbound = [];
  networkSeries = [
    {
      name: "outbound",
      data: []
    },
    {
      name: "inbound",
      data: []
    }
  ];
  memoryKernel = [];
  memoryCache = [];
  memoryFree = [];
  memoryAnon = [];
  memoryTotal = [];
  memorySeries = [
    {
      name: "kernel",
      data: []
    },
    {
      name: "cache",
      data: []
    },
    {
      name: "free",
      data: []
    },
    {
      name: "anon",
      data: []
    },
    {
      name: "total",
      data: []
    }
  ];
  cpuKernel = [];
  cpuUser = [];
  cpuIrq = [];
  cpuTotal = [];
  cpuSeries = [
    {
      name: "kernel",
      data: []
    },
    {
      name: "user",
      data: []
    },
    {
      name: "irq",
      data: []
    },
    {
      name: "total",
      data: []
    }
  ];
  storageSeries = [
    {
      data: []
    }
  ];

  setGuiderData(data) {
    this.timestamp = data["timestamp"];
    // Network
    this.outbound.push({ x: this.timestamp, y: data["network"]["outbound"] });
    this.inbound.push({ x: this.timestamp, y: data["network"]["inbound"] });
    this.networkSeries = [
      {
        name: "outbound",
        data: this.outbound
      },
      {
        name: "inbound",
        data: this.inbound
      }
    ];

    //CPU
    this.cpuKernel.push({ x: this.timestamp, y: data["cpu"]["kernel"] });
    this.cpuUser.push({ x: this.timestamp, y: data["cpu"]["user"] });
    this.cpuIrq.push({ x: this.timestamp, y: data["cpu"]["irq"] });
    this.cpuTotal.push({ x: this.timestamp, y: data["cpu"]["total"] });
    this.cpuSeries = [
      {
        name: "kernel",
        data: this.cpuKernel
      },
      {
        name: "user",
        data: this.cpuUser
      },
      {
        name: "irq",
        data: this.cpuIrq
      },
      {
        name: "total",
        data: this.cpuTotal
      }
    ];

    //Memory
    this.memoryKernel.push({ x: this.timestamp, y: data["memory"]["kernel"] });
    this.memoryCache.push({ x: this.timestamp, y: data["memory"]["cache"] });
    this.memoryFree.push({ x: this.timestamp, y: data["memory"]["free"] });
    this.memoryAnon.push({ x: this.timestamp, y: data["memory"]["anon"] });
    this.memoryTotal.push({ x: this.timestamp, y: data["memory"]["total"] });
    this.memorySeries = [
      {
        name: "kernel",
        data: this.memoryKernel
      },
      {
        name: "cache",
        data: this.memoryCache
      },
      {
        name: "free",
        data: this.memoryFree
      },
      {
        name: "anon",
        data: this.memoryAnon
      },
      {
        name: "total",
        data: this.memoryTotal
      }
    ];

    //Storage
  }
}
