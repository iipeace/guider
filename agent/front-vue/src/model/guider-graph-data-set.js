export default class GuiderGraphDataSet {
  startTimestamp = 0;
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
  networkChartOptions = {
    dataLabels: {
      enabled: false
    },
    title: {
      text: "NETWORK",
      align: "center",
      floating: false,
      style: {
        fontSize: "16px",
        color: "#263238"
      }
    },
    xaxis: {
      labels: {
        formatter: function(val) {
          return String(val).substr(5, 2);
        }
      }
    },
    yaxis: {
      min: 0,
      labels: {
        formatter: function(value) {
          return Math.floor(value / 1000) + "KB";
        }
      }
    }
  };

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
  memoryChartOptions = {
    title: {
      text: "MEMORY",
      align: "center",
      style: {
        fontSize: "16px",
        color: "#263238"
      }
    },
    chart: {
      stacked: true
    },
    dataLabels: {
      enabled: false
    },
    xaxis: {
      labels: {
        formatter: function(val) {
          return String(val).substr(5, 2);
        }
      }
    },
    yaxis: {
      labels: {
        formatter: function(value) {
          return Math.floor(value / 1000) + "GB";
        }
      }
    }
  };

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
  cpuChartOptions = {
    dataLabels: {
      enabled: false
    },
    title: {
      text: "CPU",
      align: "center",
      style: {
        fontSize: "16px",
        color: "#263238"
      }
    },
    chart: {
      stacked: true
    },
    xaxis: {
      labels: {
        formatter: function(val) {
          return String(val).substr(5, 2);
        }
      }
    },
    yaxis: {
      labels: {
        formatter: function(value) {
          return String(value).substr(0, 4) + "%";
        }
      }
    }
  };

  storageFree = [];
  storageUsage = [];
  storageSeries = [
    {
      data: []
    }
  ];
  storageChartOptions = {
    dataLabels: {
      enabled: false
    },
    title: {
      text: "STORAGE",
      align: "center",
      style: {
        fontSize: "16px",
        color: "#263238"
      }
    },
    chart: {
      stacked: true
    },
    xaxis: {
      labels: {
        formatter: function(val) {
          return String(val).substr(5, 2);
        }
      }
    },
    yaxis: {
      labels: {
        formatter: function(value) {
          return Math.floor(value / 1000) + "GB";
        }
      }
    }
  };

  addSeriesData(timestamp, list, data) {
    list.push({ x: timestamp, y: data });
  }

  setGuiderData(data) {
    this.timestamp = data["timestamp"];
    if (this.startTimestamp === 0) {
      this.startTimestamp = this.timestamp;
    }
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
    this.addSeriesData(
      this.timestamp,
      this.memoryKernel,
      data["memory"]["kernel"]
    );
    this.addSeriesData(
      this.timestamp,
      this.memoryCache,
      data["memory"]["cache"]
    );
    this.addSeriesData(this.timestamp, this.memoryFree, data["memory"]["free"]);
    this.addSeriesData(this.timestamp, this.memoryAnon, data["memory"]["anon"]);
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
    this.addSeriesData(
      this.timestamp,
      this.storageFree,
      data["storage"]["free"]
    );
    this.addSeriesData(
      this.timestamp,
      this.storageUsage,
      data["storage"]["usage"]
    );
    this.storageSeries = [
      {
        name: "free",
        data: this.storageFree
      },
      {
        name: "usage",
        data: this.storageUsage
      }
    ];
  }
}
