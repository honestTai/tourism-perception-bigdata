<template>
  <div class="container" style="padding: 6px">
    <!--景区选择-->
    <el-select v-model="query" placeholder="请选择景区" @change="handleSearchAtt">
      <el-option
        v-for="item in atts"
        :key="item.poiId"
        :label="item.name"
        :value="item.poiId"
      >
      </el-option>
    </el-select>
    <el-table
      :data="selectAtts"
      style="font-size: 16px"
      class="customer-table"
      :header-cell-style="{ textAlign: 'center' }"
      :cell-style="{ textAlign: 'center' }"
    >
      <el-table-column
        prop="name"
        label="名字"
        align="center"
        width="200px"
      >
      </el-table-column>
      <el-table-column
        prop="commentScoreNum"
        label="景区评分"
      >
      </el-table-column>
      <el-table-column prop="titleTips" label="景区类型"></el-table-column>
      <el-table-column prop="heatView" label="热度"></el-table-column>
      <el-table-column prop="address" label="地址"></el-table-column>
      <el-table-column prop="hotTags" label="关键词">
        <template slot-scope="scope">

          <el-link
            v-for="(item, index) in scope.row.hotTags.split(',')"
            :key="index"
            type="primary"
          >{{ item }}
          </el-link>
        </template>
      </el-table-column>
      <el-table-column prop="img" label="图片">
        <template slot-scope="scope">
          <img :src="scope.row.img" style="width: 100%;height: 100%">
        </template>
      </el-table-column>
      <el-table-column prop="heatView" label="热度"></el-table-column>
    </el-table>
    <!--饼状图，出行类型，得分占比-->
    <el-row :span="49" style="padding-top: 25px">
      <el-col :span="12">

        <div id="echarts3" style="height: 500px"/>
      </el-col>
      <el-col :span="12">

        <div id="echarts2" style="height: 500px"/>
      </el-col>
      <el-col :span="12">

        <div id="echarts1" style="height: 500px"/>
      </el-col>
      <el-col :span="12">

        <div id="echarts5" style="height: 500px"/>
      </el-col>
    </el-row>
    <!--趋势图：得分趋势散点；词云图：评论的词云图；具体得分占比柱状图-->
    <el-row :span="25" style="padding-top: 25px">
      <el-col :span="24">
        <div id="echarts4" style="height: 1000px" />
      </el-col>
    </el-row>
<!--    <el-row :span="25" style="padding-top: 25px">-->

<!--      <el-col :span="24">-->

<!--        <div id="echarts7" style="height: 300px"/>-->
<!--      </el-col>-->

<!--    </el-row>-->


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
      data2: [],
      data1: [],
      data: [],
      data4:[],
      words: [],
      priceTravel: [],
      score: [],
      atts: [],
      selectAtts: [],
      scoresData:[],
      query: {
        attId: String
      }
    };
  },
  created() {
    // this.getWords()
  },
  mounted() {
    // this.getAttData(this.query);
    this.getAtts()
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    getAtts() {
      recommend.attGetAll().then(res => {
        this.atts = res.data
      });
    },
    handleSearchAtt(val) {
      this.selectAtts = []
      const object = this.atts.find(item => item.poiId === val);
      this.selectAtts.push(object)
      this.getAttData({attId: val});
    },
    getAttData(data) {
      recommend.att(data).then(res => {
        this.data2 = res.data.type_data
        this.data = res.data.score_data
        this.data1 = res.data.ip_data
        this.data4 = res.data.user_data
        this.words = res.data.words
        this.scoresData = res.data.scoresData
        this.initChart();
      });
    },

    initChart() {
      let that = this
      var options5 = {
        title: {
          text: "用户类型",
          subtext: "用户类型",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: "用户类型",
            type: "pie",
            radius: "50%",
            data: this.data4,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
      var options1 = {
        title: {
          text: "地区来源",
          subtext: "地区来源",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: "地区来源",
            type: "pie",
            radius: "50%",
            data: this.data1,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
      var options3 = {
        title: {
          text: "出行分类",
          subtext: "出行分类",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: "出行分类",
            type: "pie",
            radius: "50%",
            data: this.data2,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
      var options2 = {
        title: {
          text: "得分占比",
          subtext: "得分占比",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "left",
        },
        series: [
          {
            name: "得分占比",
            type: "pie",
            radius: "50%",
            data: this.data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)",
              },
            },
          },
        ],
      };
      var option4 = {
        title: {
          text: '评论关键词'
          // x: 'center'
        },
        backgroundColor: '#fff',
        // tooltip: {
        //   pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>"
        // },
        series: [
          {
            type: 'wordCloud',
            //用来调整词之间的距离
            gridSize: 10,
            //用来调整字的大小范围
            // Text size range which the value in data will be mapped to.
            // Default to have minimum 12px and maximum 60px size.
            sizeRange: [14, 60],
            // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
            //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
            // rotationRange: [-45, 0, 45, 90],
            // rotationRange: [ 0,90],
            rotationRange: [0, 0],
            //随机生成字体颜色
            // maskImage: maskImage,
            textStyle: {
              normal: {
                color: function() {
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
              }
            },
            //位置相关设置
            // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
            // Default to be put in the center and has 75% x 80% size.
            left: 'center',
            top: 'center',
            right: null,
            bottom: null,
            width: '200%',
            height: '200%',
            //数据
            data: this.words
          }
        ]
      };
      // 按照出行次数，由高到低进行排序



      that.score = that.score.sort((a, b) => parseInt(b.score) - parseInt(a.score));
      let lines = that.score.map(item => ({value: parseInt(item.price), score: item.score, title: item.title}));

      var linesChartOption = {
        title: {
          text: '得分排名',
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
      that.$echarts
        .init(document.getElementById('echarts1')).setOption(options1)

      var wordCharts = that.$echarts
        .init(document.getElementById('echarts3'))
      wordCharts.setOption(options3)

      wordCharts.on('click', function (params) {

        that.$message.success(params.data.name + '出现次数' + params.data.value)
      });
      var wordCharts1 = that.$echarts
        .init(document.getElementById('echarts2'))
      wordCharts1.setOption(options2)

      wordCharts1.on('click', function (params) {

        that.$message.success(params.data.name + '出现次数' + params.data.value)
      });
      that.$echarts
        .init(document.getElementById('echarts5'))
        .setOption(options5);
      that.$echarts
        .init(document.getElementById('echarts4')).clear();
      that.$echarts
        .init(document.getElementById('echarts4')).setOption(option4);
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
