<template>
  <div class="container">
    <el-row :gutter="20">
      <el-col :span="10" :offset="2">
        <div class="block">
          <span class="demonstration">请选择周</span>
          <el-date-picker
            v-model="datetime"
            type="week"
            format="yyyy 第 WW 周"
            @change="weekChange"
            placeholder="选择周"
          >
          </el-date-picker>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12" :offset="1">
        <div id="echarts1" style="width: auto; height: 500px"></div>
      </el-col>
      <el-col :span="10">
        <div id="echarts2" style="width: auto; height: 400px"></div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import recommend from "@/api/tuijian/recommend";

export default {
  name: "hello",
  data() {
    return {
      datetime: "",
      options: ["娱乐", "科技"],
      item: "",
      xData: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      yData1: [120, 200, 150, 80, 70, 110, 130],
      yData2: [120, 200, 150, 80, 70, 110, 130],
      categoryPie: [
        { value: 1048, name: "Search Engine" },
        { value: 735, name: "Direct" },
        { value: 580, name: "Email" },
        { value: 484, name: "Union Ads" },
        { value: 300, name: "Video Ads" },
      ],
    };
  },
  computed: {
    ...mapGetters(["name"]),
  },
  mounted() {
    this.initecharts1();
    this.initecharts2();
  },
  created() {
    this.datetime= new Date(new Date().setDate(new Date().getDate() - new Date().getDay() + 1));
    this.queryCategory();
    this.queryPop();
  },
  methods: {
    weekChange() {
      this.queryCategory();
      this.queryPop();
    },
    queryPop(){
      var data = { datetime: this.datetime };
      recommend
        .POPTopicForWeek(data)
        .then((res) => {
          console.log(res)
          if (res.code == 20000) {
            this.xData = res.data.name;
            this.yData1 = res.data.positive;
            this.yData2 = res.data.passive;
            this.initecharts2();
          }
        })
        .catch((res) => {
          console.log(res);
        });
    },
    queryCategory() {
      var data = { datetime: this.datetime };
      recommend
        .categoryDataForWeek(data)
        .then((res) => {
          console.log(res);
          if (res.code == 20000) {
            this.categoryPie = res.data;
            this.initecharts1();
          }
        })
        .catch((res) => {
          console.log(res);
        });
    },
    initecharts1() {
      var options = {
        title: {
          text: "舆情话题分类占比",
          subtext: "舆情话题分类",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          orient: "vertical",
          left: "top",
        },
        series: [
          {
            name: "数量",
            type: "pie",
            radius: "50%",
            data: this.categoryPie,
            itemStyle: {
              normal: {
                label: {
                  show: false, //隐藏标示文字
                },
                labelLine: {
                  show: false, //隐藏标示线
                },
              },
            },
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
        .init(document.getElementById("echarts1"))
        .setOption(options);
    },
    initecharts2() {
      var option = {
        xAxis: {
          type: "category",
          data: this.xData,
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            data: this.yData1,
            type: "bar",
          },
          {
            data: this.yData2,
            type: "bar",
          },
        ],
      };
      this.$echarts.init(document.getElementById("echarts2")).setOption(option);
    },
  },
};
</script>

<style>
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
