<template>
  <div class="container" style="padding: 6px">

    <!--词云图-->
    <el-row :span="25" style="padding-top: 25px">
      <el-col :span="12">

        <div id="echarts3" style="height: 500px" />
      </el-col>
      <el-col :span="12">

        <div id="echarts2" style="height: 500px" />
      </el-col>
    </el-row>
    <!--趋势分析-->
    <el-row :span="25" style="padding-top: 25px">
      <el-col :span="24">

        <div id="echarts4" style="height: 300px" />
      </el-col>
    </el-row>

    <el-row :span="25" style="padding-top: 25px">

      <el-col :span="24">

        <div id="echarts7" style="height: 300px" />
      </el-col>

    </el-row>


  </div>
</template>

<script>
import 'echarts-wordcloud/dist/echarts-wordcloud';
import 'echarts-wordcloud/dist/echarts-wordcloud.min';
import recommend from "@/api/tuijian/recommend";
export default {
  props: {},
  data() {
    return {
      words1:[],
      words: [],
      priceTravel:[],
      score:[]
    };
  },
  created() {
    // this.getWords()
  },
  mounted() {
    this.getPriceData();
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    getPriceData() {
      recommend.priceDat().then(res => {
        console.log(res)
        this.words = res.data.feature
        this.words1 = res.data.words1
        this.priceTravel = res.data.priceTravel
        this.score = res.data.socre
        this.initChart();
      });
    },

    initChart() {
      let that = this
      var option3 = {
        title: {
          text: '游客偏好的团购特点',
          // x: 'center'
        },
        backgroundColor: '#fff',
        series: [
          {
            type: 'wordCloud',
            gridSize: 10,
            sizeRange: [14, 60],
            rotationRange: [0, 0],
            textStyle: {
              normal: {
                color: function () {
                  return (
                    'rgb(' +
                    Math.round(Math.random() * 255) +
                    ', ' +
                    Math.round(Math.random() * 255) +
                    ', ' +
                    Math.round(Math.random() * 255) +
                    ')'
                  );
                }
              },
            },
            emphasis: {
              // Customize the style when the word is clicked
              focus: 'self',
              scale: true,
              shadowBlur: 10,
              shadowColor: '#333',
              shadowOffsetX: 0,
              shadowOffsetY: 0,
              textBorderColor: '#333',
              textBorderWidth: 2,
              textPadding: 10,
              formatter: function (params) {
                console.log(params);
                return params.name + ': ' + params.value;
              }
            },
            left: 'center',
            top: 'center',
            right: null,
            bottom: null,
            width: '200%',
            height: '200%',
            data: this.words,
          }
        ]
      };
      var option4 = {
        title: {
          text: '游客偏好的路线',
          // x: 'center'
        },
        backgroundColor: '#fff',
        series: [
          {
            type: 'wordCloud',
            gridSize: 10,
            sizeRange: [14, 60],
            rotationRange: [0, 0],
            textStyle: {
              normal: {
                color: function () {
                  return (
                    'rgb(' +
                    Math.round(Math.random() * 255) +
                    ', ' +
                    Math.round(Math.random() * 255) +
                    ', ' +
                    Math.round(Math.random() * 255) +
                    ')'
                  );
                }
              },
            },
            emphasis: {
              // Customize the style when the word is clicked
              focus: 'self',
              scale: true,
              shadowBlur: 10,
              shadowColor: '#333',
              shadowOffsetX: 0,
              shadowOffsetY: 0,
              textBorderColor: '#333',
              textBorderWidth: 2,
              textPadding: 10,
              formatter: function (params) {
                console.log(params);
                return params.name + ': ' + params.value;
              }
            },
            left: 'center',
            top: 'center',
            right: null,
            bottom: null,
            width: '200%',
            height: '200%',
            data: this.words1,
          }
        ]
      };
      // 按照出行次数，由高到低进行排序
      that.priceTravel = that.priceTravel.sort((a, b) => parseInt(b.travel) - parseInt(a.travel));
      var xAxisData = that.priceTravel.map(item => item.travel); // Switch to 'travel' for x-axis
      var seriesData = that.priceTravel.map(item => ({ value: parseInt(item.price), title: item.title })); // Switch to 'price' for y-axis
      var names = that.priceTravel.map(item => item.title);

      var lineChartOption = {
        title: {
          text: '出行次数与价格趋势',
          x: 'center'
        },
        tooltip: {
          trigger: 'axis',
          formatter: function (params) {
            var data = params[0].data;
            return `标题: ${data.title}<br>出行次数: ${params[0].name}<br>价格: ${data.value}`;
          }
        },
        xAxis: {
          type: 'category',
          data: xAxisData
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: seriesData,
          type: 'line'
        }],
        dataZoom: [
          {
            type: 'slider',
            xAxisIndex: 0,
            start: 0,
            end: 100
          },
          {
            type: 'inside',
            xAxisIndex: 0,
            start: 0,
            end: 100
          }
        ]
      };


      that.score = that.score.sort((a, b) => parseInt(b.score) - parseInt(a.score));
      let lines = that.score.map(item => ({ value: parseInt(item.price), score: item.score, title: item.title }));

      var linesChartOption = {
        title: {
          text: '价格与评分趋势',
          x: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        xAxis: {
          type: 'category',
          data: lines.map(item => item.title) // Use map to extract titles
        },
        yAxis: [
          {
            type: 'value',
            name: '价格'
          },
          {
            type: 'value',
            name: '评分',
            position: 'right'
          }
        ],
        series: [
          {
            name: '价格',
            type: 'bar',
            data: lines.map(item => item.value) // Use map to extract values
          },
          {
            name: '评分',
            type: 'bar',
            yAxisIndex: 1,
            data: lines.map(item => item.score) // Use map to extract scores
          }
        ],
        dataZoom: [
          {
            type: 'slider',
            xAxisIndex: 0,
            start: 0,
            end: 100
          },
          {
            type: 'inside',
            xAxisIndex: 0,
            start: 0,
            end: 100
          }
        ]
      };


      var wordCharts =  that.$echarts
        .init(document.getElementById('echarts3'))
      wordCharts.setOption(option3)

      wordCharts.on('click',function(params){

        that.$message.success(params.data.name + '出现次数'+params.data.value)
      });
      var wordCharts1 =  that.$echarts
        .init(document.getElementById('echarts2'))
      wordCharts1.setOption(option4)

      wordCharts1.on('click',function(params){

        that.$message.success(params.data.name + '出现次数'+params.data.value)
      });
      that.$echarts
        .init(document.getElementById('echarts4'))
        .setOption(lineChartOption);
      that.$echarts
        .init(document.getElementById('echarts7'))
        .setOption(linesChartOption);
    }
  }
};
</script>

<style>
.container {
  padding: 10px;
}

.el-row {
  margin-bottom: 20px;
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
</style>
