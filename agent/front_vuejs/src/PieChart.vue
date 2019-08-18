<script>
import { Pie, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;
export default {
  extends: Pie,
  mixins: [reactiveProp],
  props: ["options"],
  mounted() {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    this.renderChart(this.chartData, this.options);
  }
};
</script>

<style lang="scss">
canvas {


}

</style>
