export class Option {
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
export class Command {
  name = "";
  helpOptions = [];

  constructor(name, helpOptions) {
    this.name = name;
    this.helpOptions = helpOptions;
  }
}

export const HotCommandDataSet = [
  new Command("top", [
    new Option("e", true, "description"),
    new Option("d", true, ""),
    new Option("o", true, ""),
    new Option("u", false, ""),
    new Option("W", false, ""),
    new Option("b", true, ""),
    new Option("T", true, ""),
    new Option("j", true, ""),
    new Option("w", true, ""),
    new Option("x", true, ""),
    new Option("X", true, ""),
    new Option("N", true, ""),
    new Option("S", true, ""),
    new Option("P", false, ""),
    new Option("I", true, ""),
    new Option("m", true),
    new Option("a", false),
    new Option("g", true),
    new Option("i", true),
    new Option("R", true),
    new Option("Q", false),
    new Option("E", true),
    new Option("H", true),
    new Option("k", true),
    new Option("z", true),
    new Option("Y", true),
    new Option("v", false)
  ]),
  new Command("disktop", []),
  new Command("nettop", []),
  new Command("filetop", []),
  new Command("systop", []),
  new Command("usertop", [])
];
