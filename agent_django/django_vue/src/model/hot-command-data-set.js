class Option {
  name = "";
  hasInput = false;
  description = "";
  input = "";

  constructor(name, hasInput, description) {
    this.name = name;
    this.hasInput = hasInput;
    this.description = description;
  }
}
class Command {
  name = "";
  helpOptions = [];

  constructor(name, helpOptions) {
    this.name = name;
    this.helpOptions = helpOptions;
  }
}

export const HotCommandDataSet = [
  new Command("top", [
    new Option(
      "e",
      true,
      "enable options\n" +
        "                a:affinity | b:block | c:cpu | C:cgroup\n" +
        "                d:disk | D:DLT | e:encode | E:Elastic\n" +
        "                f:float | F:wfc | h:sigHandler | i:irq\n" +
        "                L:cmdline | m:memory | n:net | o:oomScore\n" +
        "                p:pipe | P:perf | r:report | R:fileReport\n" +
        "                s:stack | S:pss | t:thread | u:uss\n" +
        "                w:wss | W:wchan"
    ),
    new Option(
      "d",
      true,
      "disable options\n" +
        "                a:memAvailable | A:cpuAverage\n" +
        "                c:cpu | e:encode | G:gpu | L:log\n" +
        "                p:print | t:truncate | T:task"
    ),
    new Option("o", true, "save output data"),
    new Option("u", false, "run in the background"),
    new Option("W", false, "wait for signal"),
    new Option("b", true, "set buffer size"),
    new Option("T", true, "set font path"),
    new Option("j", true, "set report path"),
    new Option("w", true, "set additional command"),
    new Option("x", true, "set local address"),
    new Option("X", true, "set request address"),
    new Option("N", true, "set report address"),
    new Option("S", true, "sort by key"),
    new Option("P", false, "group threads in same process"),
    new Option("I", true, "set input path"),
    new Option("m", true, "set terminal size"),
    new Option("a", false, "show all stats and events"),
    new Option("g", true, "set filter"),
    new Option("i", true, "set interval"),
    new Option("R", true, "set repeat count"),
    new Option("Q", false, "print all rows in a stream"),
    new Option("E", true, "set cache dir path"),
    new Option("H", true, "set function depth level"),
    new Option("k", true, "set kill list"),
    new Option("z", true, "set cpu affinity list"),
    new Option("Y", true, "set sched priority list"),
    new Option("v", false, "verbose")
  ]),
  new Command("disktop", [
    new Option(
      "e",
      true,
      "enable options\n" +
        "                a:affinity | b:block | c:cpu | C:cgroup\n" +
        "                d:disk | D:DLT | e:encode | E:Elastic\n" +
        "                f:float | F:wfc | h:sigHandler | i:irq\n" +
        "                L:cmdline | m:memory | n:net | o:oomScore\n" +
        "                p:pipe | P:perf | r:report | R:fileReport\n" +
        "                s:stack | S:pss | t:thread | u:uss\n" +
        "                w:wss | W:wchan"
    ),
    new Option(
      "d",
      true,
      "disable options\n" +
        "                a:memAvailable | A:cpuAverage\n" +
        "                c:cpu | e:encode | G:gpu | L:log\n" +
        "                p:print | t:truncate | T:task"
    ),
    new Option("o", true, "save output data"),
    new Option("u", false, "run in the background"),
    new Option("W", false, "wait for signal"),
    new Option("b", true, "set buffer size"),
    new Option("T", true, "set font path"),
    new Option("j", true, "set report path"),
    new Option("w", true, "set additional command"),
    new Option("x", true, "set local address"),
    new Option("X", true, "set request address"),
    new Option("N", true, "set report address"),
    new Option("S", true, "sort by key"),
    new Option("P", false, "group threads in same process"),
    new Option("I", true, "set input path"),
    new Option("m", true, "set terminal size"),
    new Option("a", false, "show all stats and events"),
    new Option("g", true, "set filter"),
    new Option("i", true, "set interval"),
    new Option("R", true, "set repeat count"),
    new Option("Q", false, "print all rows in a stream"),
    new Option("E", true, "set cache dir path"),
    new Option("H", true, "set function depth level"),
    new Option("k", true, "set kill list"),
    new Option("z", true, "set cpu affinity list"),
    new Option("Y", true, "set sched priority list"),
    new Option("v", false, "verbose")
  ]),
  new Command("nettop", [
    new Option(
      "e",
      true,
      "enable options\n" +
        "                a:affinity | b:block | c:cpu | C:cgroup\n" +
        "                d:disk | D:DLT | e:encode | E:Elastic\n" +
        "                f:float | F:wfc | h:sigHandler | i:irq\n" +
        "                L:cmdline | m:memory | n:net | o:oomScore\n" +
        "                p:pipe | P:perf | r:report | R:fileReport\n" +
        "                s:stack | S:pss | t:thread | u:uss\n" +
        "                w:wss | W:wchan"
    ),
    new Option(
      "d",
      true,
      "disable options\n" +
        "                a:memAvailable | A:cpuAverage\n" +
        "                c:cpu | e:encode | G:gpu | L:log\n" +
        "                p:print | t:truncate | T:task"
    ),
    new Option("o", true, "save output data"),
    new Option("u", false, "run in the background"),
    new Option("W", false, "wait for signal"),
    new Option("b", true, "set buffer size"),
    new Option("T", true, "set font path"),
    new Option("j", true, "set report path"),
    new Option("w", true, "set additional command"),
    new Option("x", true, "set local address"),
    new Option("X", true, "set request address"),
    new Option("N", true, "set report address"),
    new Option("S", true, "sort by key"),
    new Option("P", false, "group threads in same process"),
    new Option("I", true, "set input path"),
    new Option("m", true, "set terminal size"),
    new Option("a", false, "show all stats and events"),
    new Option("g", true, "set filter"),
    new Option("i", true, "set interval"),
    new Option("R", true, "set repeat count"),
    new Option("Q", false, "print all rows in a stream"),
    new Option("E", true, "set cache dir path"),
    new Option("H", true, "set function depth level"),
    new Option("k", true, "set kill list"),
    new Option("z", true, "set cpu affinity list"),
    new Option("Y", true, "set sched priority list"),
    new Option("v", false, "verbose")
  ]),
  new Command("filetop", [
    new Option(
      "e",
      true,
      "enable options\n" + "                p:pipe | e:encode"
    ),
    new Option(
      "d",
      true,
      "disable options\n" + "                e:encode | p:print"
    ),
    new Option("o", true, "save output data"),
    new Option("u", false, "run in the background"),
    new Option("W", false, "wait for signal"),
    new Option("b", true, "set buffer size"),
    new Option("w", true, "set additional command"),
    new Option("x", true, "set local address"),
    new Option("X", true, "set request address"),
    new Option("N", true, "set report address"),
    new Option("S", true, "sort by key"),
    new Option("m", true, "set terminal size"),
    new Option("a", false, "show all stats and events"),
    new Option("g", true, "set filter"),
    new Option("i", true, "set interval"),
    new Option("R", true, "set repeat count"),
    new Option("Q", false, "print all rows in a stream"),
    new Option("E", true, "set cache dir path"),
    new Option("k", true, "set kill list"),
    new Option("z", true, "set cpu affinity list"),
    new Option("Y", true, "set sched priority list"),
    new Option("v", false, "verbose")
  ]),
  new Command("systop", [
    new Option(
      "e",
      true,
      "enable options\n" +
        "                a:affinity | b:block | c:cpu | C:cgroup\n" +
        "                d:disk | D:DLT | e:encode | E:Elastic\n" +
        "                f:float | F:wfc | h:sigHandler | i:irq\n" +
        "                L:cmdline | m:memory | n:net | o:oomScore\n" +
        "                p:pipe | P:perf | r:report | R:fileReport\n" +
        "                s:stack | S:pss | t:thread | u:uss\n" +
        "                w:wss | W:wchan"
    ),
    new Option(
      "d",
      true,
      "disable options\n" +
        "                a:memAvailable | A:cpuAverage\n" +
        "                c:cpu | e:encode | G:gpu | L:log\n" +
        "                p:print | t:truncate | T:task"
    ),
    new Option("o", true, "save output data"),
    new Option("u", false, "run in the background"),
    new Option("W", false, "wait for signal"),
    new Option("b", true, "set buffer size"),
    new Option("T", true, "set font path"),
    new Option("j", true, "set report path"),
    new Option("w", true, "set additional command"),
    new Option("x", true, "set local address"),
    new Option("X", true, "set request address"),
    new Option("N", true, "set report address"),
    new Option("S", true, "sort by key"),
    new Option("P", false, "group threads in same process"),
    new Option("I", true, "set input path"),
    new Option("m", true, "set terminal size"),
    new Option("a", false, "show all stats and events"),
    new Option("g", true, "set filter"),
    new Option("i", true, "set interval"),
    new Option("R", true, "set repeat count"),
    new Option("Q", false, "print all rows in a stream"),
    new Option("E", true, "set cache dir path"),
    new Option("H", true, "set function depth level"),
    new Option("k", true, "set kill list"),
    new Option("z", true, "set cpu affinity list"),
    new Option("Y", true, "set sched priority list"),
    new Option("v", false, "verbose")
  ]),
  new Command("usertop", [
    new Option(
      "e",
      true,
      "enable options\n" +
        "                a:affinity | b:block | c:cpu | C:cgroup\n" +
        "                d:disk | D:DLT | e:encode | E:Elastic\n" +
        "                f:float | F:wfc | h:sigHandler | i:irq\n" +
        "                L:cmdline | m:memory | n:net | o:oomScore\n" +
        "                p:pipe | P:perf | r:report | R:fileReport\n" +
        "                s:stack | S:pss | t:thread | u:uss\n" +
        "                w:wss | W:wchan"
    ),
    new Option(
      "d",
      true,
      "disable options\n" +
        "                a:memAvailable | A:cpuAverage\n" +
        "                c:cpu | e:encode | G:gpu | L:log\n" +
        "                p:print | t:truncate | T:task"
    ),
    new Option("o", true, "save output data"),
    new Option("u", false, "run in the background"),
    new Option("W", false, "wait for signal"),
    new Option("b", true, "set buffer size"),
    new Option("T", true, "set font path"),
    new Option("j", true, "set report path"),
    new Option("w", true, "set additional command"),
    new Option("x", true, "set local address"),
    new Option("X", true, "set request address"),
    new Option("N", true, "set report address"),
    new Option("S", true, "sort by key"),
    new Option("P", false, "group threads in same process"),
    new Option("I", true, "set input path"),
    new Option("m", true, "set terminal size"),
    new Option("a", false, "show all stats and events"),
    new Option("g", true, "set filter"),
    new Option("i", true, "set interval"),
    new Option("R", true, "set repeat count"),
    new Option("Q", false, "print all rows in a stream"),
    new Option("E", true, "set cache dir path"),
    new Option("H", true, "set function depth level"),
    new Option("k", true, "set kill list"),
    new Option("z", true, "set cpu affinity list"),
    new Option("Y", true, "set sched priority list"),
    new Option("v", false, "verbose")
  ])
];
