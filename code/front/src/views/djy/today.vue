<template>
  <div class="dashboard-container">


    <el-row>
      <el-col>
        路线总数
        <el-link type="primary">{{ amount.total_merchants }}</el-link>
        3分及以下
        <el-link type="primary">{{ amount.low_score_merchants }}</el-link>
        4分及以上
        <el-link type="primary">{{ amount.high_score_merchants }}</el-link>
        ，得分为3分路线占比
        <el-link type="primary">{{ amount.rate_of_3_score }}</el-link>
        ，得分为4分路线占比
        <el-link type="primary">{{ amount.rate_of_4_score }}</el-link>
      </el-col>
    </el-row>
    <el-row>
      <el-col :offset="1" :span="13">
        <div class="" style="">
          <el-table
            :data="tableData"
            style="font-size: 16px"
            height="985px"
            class="customer-table"
            :header-cell-style="{ textAlign: 'center' }"
            :cell-style="{ textAlign: 'center' }"
          >
            <!-- <el-table-column type="index" width="50"> </el-table-column> -->
            <el-table-column prop="image" label="图片">
              <template slot-scope="scope">
                <img
                  :src="scope.row.img"
                  width="150"
                  height="150px"
                >
                </img>
              </template>
            </el-table-column>
            <el-table-column
              prop="title"
              label="标题"
              align="center"
              width="200px"
            >
            </el-table-column>
            <el-table-column prop="name" label="特色">
              <template slot-scope="scope">

                  <el-link
                    v-for="(item, index) in scope.row.feature.split(',')"
                    :key="index"
                    type="primary"
                  >{{ item }}</el-link>
              </template>
            </el-table-column>
            <el-table-column
              prop="price"
              label="价格"
            >
            </el-table-column>
            <el-table-column prop="score" label="评分"> </el-table-column>
            <el-table-column prop="travel" label="出行次数"> </el-table-column>
             <el-table-column prop="comment" label="评论数量"> </el-table-column>
          </el-table>
        </div>
      </el-col>
      <el-col :offset="1" :span="8">
        <el-row>
          <div id="echarts1" style="height: 450px; width: 100%"></div>
        </el-row>
        <el-row>
          <div id="echarts2" style="height: 450px; width: 100%"></div>
        </el-row>
      </el-col>
    </el-row>
    <wordcloud></wordcloud>

  </div>
</template>

<script>
import { mapGetters } from "vuex";
import recommend from "@/api/tuijian/recommend";
import Wordcloud from "@/views/djy/wordcloud.vue";

export default {
  name: "Dashboard",
  components: {Wordcloud},
  data() {
    return {
      drawer: false,
      activeNames1: "",
      activeNames2: "",
      named_entity: [],
      sentimentData: {},
      subjects: {},
      topicInfo: {
        image: "",
        summary: "",
        name: "",
        ori_uv: "35264",
        r: "78541",
        m: "77587",
      },
      university: [],
      amount: {},
      currentTopic: "",
      direction: "rtl",
      tableData: [],
    };
  },
  computed: {
    ...mapGetters(["name"]),
  },
  mounted() {
    this.getData();
  },
  created() {

  },
  methods: {
    initecharts1() {
      var options = {
        series: [
          {
            type: "gauge",
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 1,
            splitNumber: 8,
            axisLine: {
              lineStyle: {
                width: 6,
                color: [
                  [0.25, "#FF6E76"],
                  [0.5, "#FDDD60"],
                  [0.75, "#58D9F9"],
                  [1, "#7CFFB2"],
                ],
              },
            },
            pointer: {
              icon: "path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",
              length: "12%",
              width: 20,
              offsetCenter: [0, "-60%"],
              itemStyle: {
                color: "auto",
              },
            },
            axisTick: {
              length: 12,
              lineStyle: {
                color: "auto",
                width: 2,
              },
            },
            splitLine: {
              length: 20,
              lineStyle: {
                color: "auto",
                width: 5,
              },
            },
            axisLabel: {
              color: "#464646",
              fontSize: 20,
              distance: -60,
              formatter: function (value) {
                if (value === 0.875) {
                  return "A";
                } else if (value === 0.625) {
                  return "B";
                } else if (value === 0.375) {
                  return "C";
                } else if (value === 0.125) {
                  return "D";
                }
                return "";
              },
            },
            title: {
              offsetCenter: [0, "-30%"],
              fontSize: 30,
            },
            detail: {
              fontSize: 50,
              offsetCenter: [0, "0%"],
              valueAnimation: true,
              formatter: function (value) {
                return Math.round(value * 100) + "%";
              },
              color: "auto",
            },
            data: [
              {
                value:  this.amount.rate_of_3_score.replace("%","")/100,
                name: "3分占比",
              },
            ],
          },
        ],
      };
      this.$echarts.init(document.getElementById("echarts1")).setOption(options);
    },
    initecharts2() {
      var options = {
        series: [
          {
            type: "gauge",
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 1,
            splitNumber: 8,
            axisLine: {
              lineStyle: {
                width: 6,
                color: [
                  [0.25, "#FF6E76"],
                  [0.5, "#FDDD60"],
                  [0.75, "#58D9F9"],
                  [1, "#7CFFB2"],
                ],
              },
            },
            pointer: {
              icon: "path://M12.8,0.7l12,40.1H0.7L12.8,0.7z",
              length: "12%",
              width: 20,
              offsetCenter: [0, "-60%"],
              itemStyle: {
                color: "auto",
              },
            },
            axisTick: {
              length: 12,
              lineStyle: {
                color: "auto",
                width: 2,
              },
            },
            splitLine: {
              length: 20,
              lineStyle: {
                color: "auto",
                width: 5,
              },
            },
            axisLabel: {
              color: "#464646",
              fontSize: 20,
              distance: -60,
              formatter: function (value) {
                if (value === 0.875) {
                  return "A";
                } else if (value === 0.625) {
                  return "B";
                } else if (value === 0.375) {
                  return "C";
                } else if (value === 0.125) {
                  return "D";
                }
                return "";
              },
            },
            title: {
              offsetCenter: [0, "-30%"],
              fontSize: 30,
            },
            detail: {
              fontSize: 50,
              offsetCenter: [0, "0%"],
              valueAnimation: true,
              formatter: function (value) {
                return Math.round(value * 100) + "%";
              },
              color: "auto",
            },
            data: [
              {
                value:  this.amount.rate_of_4_score.replace("%","")/100,
                name: "4分占比",
              },
            ],
          },
        ],
      };
      this.$echarts.init(document.getElementById("echarts2")).setOption(options);
    },
    timestampToTime(row) {
      var timestamp = row.create_at;
      //时间戳为10位需*1000，时间戳为13位的话不需乘1000
      var date = new Date(timestamp * 1000);
      var Y = date.getFullYear() + "-";
      var M =
        (date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1) + "-";
      var D = date.getDate() + " ";
      var h = date.getHours() + ":";
      var m = date.getMinutes() + ":";
      var s = date.getSeconds();
      return Y + M + D + h + m + s;
    },
    topicResolve(topic) {
      this.currentTopic = topic;
      // let data = { topic: item };
      this.getTopicSubject(topic);
    },
    getTopicSubject(topic) {
      this.drawer = true;
      let data = { topic: topic };
      console.log(data);
      recommend.calculateTopic(data).then((res) => {
        if (res.code == 20000) {
          this.topicInfo = res.topic;
          this.subjects = res.subject;
          this.sentimentData = res.sentiment;
        }
      });
    },
    getData() {
      const data = {};
      recommend
        .recentlyWeek(data)
        .then((response) => {
          if (response.code == 20000) {
            // console.log(response)
            this.tableData = response.buyings;
            this.amount = response.amount;
            this.initecharts1();
            this.initecharts2();
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
<style>
.el-table td,
th.is-leaf {
  border-bottom: 0px;
}
table {
  border-bottom: 0px;
}
a {
  text-decoration: none;
  color: blue;
}
.el-drawer.rtl {
  overflow: scroll;
}
</style>
