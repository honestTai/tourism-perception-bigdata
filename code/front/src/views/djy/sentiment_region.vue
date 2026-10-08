<template>
  <div class="container">
    <el-row>
      <el-col :span="12" :offset="1">
        <div
          id="echarts1"
          :class="className"
          style="height: 800px; width: 100%"
        />
      </el-col>
      <el-col :span="10">
        <el-row>
          <div id="echarts2" style="width: auto; height: 400px"></div>
        </el-row>
        <el-row>
          <div id="echarts3" style="width: auto; height: 400px"></div>
        </el-row>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import recommend from "@/api/tuijian/recommend";

export default {
  props: {
    className: {
      type: String,
      default: "chart",
    },
    id: {
      type: String,
      default: "chart",
    },
    width: {
      type: String,
      default: "100%",
    },
    height: {
      type: String,
      default: "800px",
    },

    title: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      chart: null,
      datetime: "",
      province: [],
      data1: [],
      data2: [],
      data3: [],
    };
  },
  mounted() {
    var chinaMap = require("/src/data/china.json");
    this.$echarts.registerMap("china", { geoJSON: chinaMap });
    this.initChart();
    this.initecharts2();
    this.initecharts3();
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  created() {
    this.datetime= new Date(new Date().setDate(new Date().getDate() - new Date().getDay() + 1));
    this.getRegionData();
  },
  methods: {
    weekChange() {
      this.getRegionData();
    },
    randomValue() {
      return Math.round(Math.random() * 1000);
    },
    getRegionData() {
      var data = { datetime: this.datetime };
      recommend.regionData(data).then((res) => {
        if (res.code == 20000) {
          this.data1 = res.data.map;
          this.province = res.data.province;
          this.initChart();
          // console.log(res);
        }
      });
    },
    initecharts2() {
      var options = {
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
            name: "Access From",
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
      this.$echarts
        .init(document.getElementById("echarts2"))
        .setOption(options);
    },
    initecharts3() {

      this.chart = this.$echarts.init(document.getElementById("echarts3"));
      var option = {
        title: {
          text: this.title,
          x: "center",
        },
        backgroundColor: "#fff",
        // tooltip: {
        //   pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>"
        // },
        series: [
          {
            type: "wordCloud",
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
                color: function () {
                  return (
                    "rgb(" +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ", " +
                    Math.round(Math.random() * 255) +
                    ")"
                  );
                },
              },
            },
            //位置相关设置
            // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
            // Default to be put in the center and has 75% x 80% size.
            left: "center",
            top: "center",
            right: null,
            bottom: null,
            width: "200%",
            height: "200%",
            //数据
            data: this.data3,
          },
        ],
      };
      this.chart.setOption(option);
    },
    initChart() {
      this.chart = this.$echarts.init(document.getElementById("echarts1"));
      this.chart.on("click", (param) => {
        // alert(param.name);
        for (var i in this.province) {
          console.log(this.province[i]["name"] === param.name);
          if (this.province[i]["name"] === param.name) {
            console.log(this.province[i])
            this.data2 = this.province[i].pieCount;
            this.data3 = this.province[i].wordCount;
            this.initecharts2();
            this.initecharts3();
          }
        }
      });
      var option = {
        tooltip: {
          formatter: function (params, ticket, callback) {
            if (!params.value) {
              params.value = "-";
            }
            return (
              params.seriesName + "<br />" + params.name + ":" + params.value
            );
          }, //数据格式化
        },
        visualMap: {
          min: 0,
          max: 1500,
          left: "left",
          top: "top",
          text: ["高", "低"], //取值范围的文字
          inRange: {
            color: ["#e0ffff", "#006edd"], //取值范围的颜色
          },
          show: true, //图注
        },
        geo: {
          map: "china",
          roam: false, //不开启缩放和平移
          zoom: 1.13, //视角缩放比例
          label: {
            normal: {
              show: true,
              fontSize: "10",
              color: "rgba(0,0,0,0.7)",
            },
          },
          itemStyle: {
            normal: {
              borderColor: "rgba(0, 0, 0, 0.2)",
            },
            emphasis: {
              areaColor: "#F3B329", //鼠标选择区域颜色
              shadowOffsetX: 0,
              shadowOffsetY: 0,
              shadowBlur: 20,
              borderWidth: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },
          },
        },
        series: [
          {
            name: "出行人数",
            type: "map",
            geoIndex: 0,
            data: this.data1,
            // 自定义名称映射
            nameMap: {},
          },
        ],
      };
      this.chart.setOption(option); //跟新图表
    },
  },
};
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
  margin-top: 99px;
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
