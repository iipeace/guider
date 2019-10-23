<template>
  <div>
    <b-card no-body>
      <b-card-body>
        <b-row>
          <b-col sm="6">
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
                  <b-form-input
                    list="my-list-id"
                    v-model="command"
                  ></b-form-input>

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
                <b-btn v-if="!requestId" size="sm" @click="sendCommand"
                  >Launch</b-btn
                >
                <b-btn v-else size="sm" @click="stopCommandRun">Stop</b-btn>
                <b-button
                  size="sm"
                  @click="$bvModal.show(`modal-scrollable-${index}`)"
                  >History</b-button
                >
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
          </b-col>
          <b-col>
            <h4>Output</h4>
            <code v-html="data"></code>
          </b-col>
        </b-row>
      </b-card-body>
    </b-card>

    <b-modal
      :id="`modal-scrollable-${index}`"
      body-bg-variant="info"
      scrollable
      hide-footer
    >
      <template slot="modal-title">
        <h3 style="color: black">Command-{{ index + 1 }} Histories</h3>
      </template>
      <h4 v-for="(command, index) in commandHistory" :key="command">
        {{ index + 1 }}. {{ command }}
      </h4>
    </b-modal>
  </div>
</template>

<script>
import { HotCommandDataSet } from "../model/hot-command-data-set";
import { mapState } from "vuex";

export default {
  props: {
    index: Number
  },
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
    },
    ...mapState(["server"])
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
      if (!this.server.hasTargetAddr()) {
        alert("please set target address");
        return false;
      }
      if (this.requestId !== "") {
        this.stopCommandRun();
      }
      this.requestId = `${this.fullCommand}-${new Date().getTime()}`;

      this.sockets.subscribe(this.requestId, data => {
        if (data.result === 0) {
          this.data = data.data;
        } else if (data.result < 0) {
          alert(data.errorMsg);
        }
      });

      this.sockets.subscribe(`${this.requestId}_stop`, data => {
        if (data.result === 0) {
          this.close();
        } else if (data.result < 0) {
          alert(data.errorMsg);
        }
      });

      this.$socket.emit(
        "get_data_by_command",
        this.server.targetAddr,
        this.requestId,
        this.fullCommand
      );
      this.commandHistory.push(this.fullCommand);
    },
    stopCommandRun() {
      this.$socket.emit("stop_command_run", this.requestId);
      this.close();
    },
    close() {
      this.sockets.unsubscribe(this.requestId);
      this.sockets.unsubscribe(`${this.requestId}_stop`);
      this.requestId = "";
    }
  },
  beforeDestroy() {
    if (this.requestId) {
      this.stopCommandRun();
    }
  }
};
</script>

<style scoped></style>
