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
              description="Enter guider command"
              label="Enter command"
              label-for="input-horizontal"
            >
              <b-form-input
                id="input-horizontal"
                v-model="command"
              ></b-form-input>
            </b-form-group>
          </b-col>
          <b-col>
            <b-btn @click="sendCommand">Launch</b-btn>
          </b-col>
        </b-row>
        <b-row>
          <b-col>
            <b-form-group label="Quick command">
              <b-form-radio-group
                v-model="selected"
                :options="options"
                name="radios-stacked"
                stacked
              ></b-form-radio-group>
            </b-form-group>

          </b-col>
        </b-row>
      </b-card-body>
      <b-card-footer>
        <h5>Result</h5>
        <p>
          {{ data }}
        </p>
      </b-card-footer>
    </b-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      command: "",
      data: {},
      selected: 'first',
      options: [
        { text: 'First radio', value: 'first' },
        { text: 'Second radio', value: 'second' },
        { text: 'Third radio', value: 'third' }
      ]
    };
  },
  methods: {
    sendCommand() {

    }
  }
};
</script>

<style scoped></style>
