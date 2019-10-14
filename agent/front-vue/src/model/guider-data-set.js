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
  memorySeries = [
    {
      name: "free",
      data: []
    },
    {
      name: "cache",
      data: []
    },
    {
      name: "kernel",
      data: []
    },
    {
      name: "anon",
      data: []
    }
  ];
  cpuKernel = [];
  cpuUser = [];
  cpuIrq = [];
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
      }
    ];

    //Memory
    this.memoryKernel.push({ x: this.timestamp, y: data["memory"]["kernel"] });
    this.memoryCache.push({ x: this.timestamp, y: data["memory"]["cache"] });
    this.memoryFree.push({ x: this.timestamp, y: data["memory"]["free"] });
    this.memoryAnon.push({ x: this.timestamp, y: data["memory"]["anon"] });
    this.memorySeries = [
      {
        name: "free",
        data: this.memoryFree
      },
      {
        name: "cache",
        data: this.memoryCache
      },
      {
        name: "kernel",
        data: this.memoryKernel
      },
      {
        name: "anon",
        data: this.memoryAnon
      }
    ];

    //Storage
  }
}
