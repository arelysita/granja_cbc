<template>
  <div class="bar-chart">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'BarChart',
  props: {
    chartData: {
      type: Object,
      required: true
    },
    options: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
    const chartCanvas = ref(null)
    let chartInstance = null

    const defaultOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }

    const initChart = () => {
      if (chartCanvas.value) {
        const ctx = chartCanvas.value.getContext('2d')
        
        if (chartInstance) {
          chartInstance.destroy()
        }

        chartInstance = new Chart(ctx, {
          type: 'bar',
          data: props.chartData,
          options: { ...defaultOptions, ...props.options }
        })
      }
    }

    onMounted(() => {
      initChart()
    })

    watch(() => props.chartData, () => {
      initChart()
    }, { deep: true })

    return {
      chartCanvas
    }
  }
}
</script>

<style scoped>
.bar-chart {
  height: 300px;
  width: 100%;
}
</style>