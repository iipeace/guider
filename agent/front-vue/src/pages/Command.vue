<template>
  <div>
    <b-card no-body>
      <b-card-header>
        <h4>Command</h4>
      </b-card-header>
      <b-card-body>
        <b-row>
          <b-col sm="8">
            <b-form-group
              id="fieldset-horizontal"
              label-cols-sm="4"
              label-cols-lg="3"
              :description="fullCommand"
              label="Enter command"
              label-for="input-horizontal"
            >
              <b-form-input list="my-list-id" v-model="command"></b-form-input>

              <datalist id="my-list-id">
                <option
                  v-for="command in hotCommandDataSet"
                  :key="command.name"
                  >{{ command.name }}</option
                >
              </datalist>
            </b-form-group>
          </b-col>
          <b-col>
            <b-btn @click="sendCommand">Launch</b-btn>
            <b-button v-b-modal.modal-scrollable>History</b-button>
          </b-col>
        </b-row>
        <div>
          <b-form-group label="Command Help">
            <b-form-checkbox-group
              v-model="selectedOptions"
              name="flavour-2a"
              stacked
            >
              <b-row
                v-for="option in options.values()"
                :value="option"
                :key="option.name"
                class="mt-1"
              >
                <b-col sm="1">
                  <b-form-checkbox :value="option.name">
                    {{ option.name }}
                  </b-form-checkbox>
                </b-col>
                <b-col sm="3">
                  <b-form-input
                    v-if="option.hasInput"
                    size="sm"
                    v-model="option.input"
                    trim
                  ></b-form-input>
                </b-col>
                <b-col>
                  <span>{{ option.description }}</span>
                </b-col>
              </b-row>
            </b-form-checkbox-group>
          </b-form-group>
        </div>
      </b-card-body>
      <b-card-footer>
        <h5>Result</h5>
        <p>
          {{ data }}
        </p>
      </b-card-footer>
    </b-card>

    <b-modal id="modal-scrollable" scrollable ok-only title="Command Histories">
      <span
        class="my-4"
        v-for="(command, index) in commandHistory"
        :key="command"
      >
        {{ index + 1 }}. {{ command }}
      </span>
    </b-modal>
  </div>
</template>

<script>
  import {HotCommandDataSet} from "../model/hot-command-data-set";

  export default {
  data() {
    return {
      command: "",
      data: {},
      selectedOptions: [],
      options: [],
      hotCommandDataSet: [],
      helpOptionsMap: new Map(),
      requestId: "",
      commandHistory: []
    };
  },
  computed: {
    fullCommand: function() {
      let detailCommand = "";
      const options = this.helpOptionsMap.get(this.command);
      if (this.selectedOptions) {
        this.selectedOptions.forEach(s => {
          const option = options.get(s);
          detailCommand += `-${option.name} ${option.input} `;
        });
      }

      return `GUIDER ${this.command} ${detailCommand}`;
    }
  },
  created() {
    this.init();
  },
  watch: {
    command: function(val) {
      if (this.helpOptionsMap.has(val)) {
        this.options = this.helpOptionsMap.get(val);
      }
    }
  },
  methods: {
    init() {
      this.hotCommandDataSet = HotCommandDataSet;
      this.hotCommandDataSet.forEach(d => {
        const optionMap = new Map();
        d.helpOptions.forEach(o => {
          optionMap.set(o.name, o);
        });
        this.helpOptionsMap.set(d.name, optionMap);
      });
    },
    sendCommand() {
      if (!this.$store.getters.hasTargetAddr) {
        alert("please set target address");
        return false;
      }
      if (this.requestId !== "") {
        this.StopCommandRun();
      }
      this.requestId = "command" + String(new Date());
      this.$socket.emit(
        "get_data_by_command",
        this.$store.getters.getTargetAddr,
        this.requestId,
        this.fullCommand
      );
      this.commandHistory.push(this.fullCommand);
    },
    StopCommandRun() {
      this.$socket.emit("stop_command_run", this.requestId);
      this.requestId = "";
    }
  },
  beforeDestroy() {
    this.StopCommandRun();
  },
  sockets: {
    set_command_data: function(data) {
      if (data.result === 0) {
        this.data = data.data;
      } else if (data.result < 0) {
        alert(data.errorMsg);
      }
    }
  }
};
</script>

<style scoped></style>
