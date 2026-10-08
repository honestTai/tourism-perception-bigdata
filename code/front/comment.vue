<template>
  <div class="container" style="padding: 6px">
    <el-row style="">
      <el-input v-model="emotionText" style="width:200px;" placeholder="请输入话题名称"></el-input>
      <el-button type="primary" @click="getEmotion" >情感倾向查看</el-button>
      <br/>
      <el-link style="font-size: 21px; padding: 10px">
        {{summary}}
      </el-link>
      <el-col>
        <el-select
          v-model="university_name"
          filterable
          @change="handleBlur1"
          placeholder="请选择"
        >
          <el-option
            v-for="item in university"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </el-col>
    </el-row>
    <el-row :span="25" style="padding-top: 25px">
      <div>
        <el-col :span="4">
          <el-link type="primary" style="font-size: 35px"
            >评论总量{{ total_count }}条</el-link
          >
        </el-col>
        <el-col :span="4">
          <el-link type="primary" style="font-size: 35px"
            >正面评论{{ po_count }}条</el-link
          >
        </el-col>
        <el-col :span="4">
          <el-link type="primary" style="font-size: 35px"
            >中性评论{{ ne_count }}条</el-link
          >
        </el-col>
        <el-col :span="4">
          <el-link type="primary" style="font-size: 35px"
            >负面评论{{ pa_count }}条</el-link
          >
        </el-col>
        <el-col :span="5" :offset="1">
          <el-link v-if="pa_count>po_count*0.4" type="danger" style="font-size: 35px"
            >负面评论预警<i class="el-icon-warning"></i
          ></el-link>
        </el-col>
      </div>
    </el-row>
    <el-row :span="25" style="padding-top: 25px">
      <el-col :span="8">

        <div id="echarts1" style="height: 300px" />
      </el-col>
      <el-col :span="5">
        <el-link type="" style="font-size: 18px; font-weight: bold"></el-link>
        <div id="circle1" style="height: 400px" />
      </el-col>
      <el-col :span="8">

        <div id="echarts2" style="height: 300px" />
      </el-col>
    </el-row>
    <el-row :span="25" style="padding-top: 25px">
      <el-col :span="10">
          <el-link type="" style="font-size: 18px; font-weight: bold"
          >正面评论top</el-link
        >
        <el-table
          :data="po_data"
          style="font-size: 16px"
          class="customer-table"
          :header-cell-style="{ textAlign: 'center' }"
          :cell-style="{ textAlign: 'center' }"
        >
          <el-table-column
            prop="text"
            label="内容"
            align="center"
            width="200px"
          >
          </el-table-column>
          <el-table-column
            prop="created_at"
            label="发布时间"
          >
          </el-table-column>
          <el-table-column prop="like_count" label="点赞数"> </el-table-column>
          <el-table-column prop="screen_name" label="用户"> </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="10" :offset="2">
          <el-link type="" style="font-size: 18px; font-weight: bold"
          >负面评论top</el-link
        >
        <el-table
          :data="pa_data"
          style="font-size: 16px"
          class="customer-table"
          :header-cell-style="{ textAlign: 'center' }"
          :cell-style="{ textAlign: 'center' }"
        >
          <!-- <el-table-column type="index" width="50"> </el-table-column> -->
          <el-table-column
            prop="text"
            label="内容"
            align="center"
            width="200px"
          >
          </el-table-column>
          <el-table-column
            prop="created_at"
            label="发布时间"
          >
          </el-table-column>
          <el-table-column prop="screen_name" label="用户"> </el-table-column>
          <el-table-column prop="like_count" label="点赞数"> </el-table-column>
          <!-- <el-table-column prop="ori_uv" label="原创人数"> </el-table-column> -->
        </el-table>
      </el-col>
    </el-row>

  </div>
</template>

<script>
import "echarts-wordcloud/dist/echarts-wordcloud";
import "echarts-wordcloud/dist/echarts-wordcloud.min";
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
      default: "789px",
    },
    title: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      chart: null,
      total_count: 0,
      po_count: 0,
      ne_count: 0,
      pa_count: 0,
      topic: "",
      wordData: [

      ],
      wordData1: [],
      wordData2: [],
      summary:'',
      top_pa: [],
      top_po: [],
      pa_data:[],
      po_data: [],
      university: [],
      university_name:'',
      emotionText:''
    };
  },
created() {
  this.getUniversity();
},
  mounted() {
    this.getWords();
    this.initChart();
  },
  beforeDestroy() {
    if (!this.chart) {
      return;
    }
    this.chart.dispose();
    this.chart = null;
  },
  methods: {
    getEmotion(){
      var data = { word: this.emotionText };
      recommend
        .emotion(data)
        .then((res) => {
          if (res.code == 20000) {
            this.$message.info("情感分数为："+res.data)
          }
          if(res.code == 20001){

          }
        })
    },
    handleBlur1() {
      // console.log(this.university_name)
      this.getWords();
    },
    getUniversity() {
      const data = {};
      recommend.universityParam(data).then((response) => {
        if (response.code == 20000) {
          this.university = response.data;
          console.log(this.university.slice(0, 20));
        }
      });
    },
    getWords() {
      var data = { subject: this.university_name };
      console.log(data)
      recommend
        .allComments(data)
        .then((res) => {
          if (res.code == 20000) {
              console.log(res.data.word)
            // this.summary = res.data.summary;
            this.total_count = res.data.total;
            this.po_count = res.data.positive;
            this.ne_count = res.data.neutral;
            this.pa_count = res.data.passive;
            this.pa_data = res.data.pa_top;
            this.po_data = res.data.po_top;
            this.wordData1 = res.data.word;
            this.wordData2 = res.data.word2;
            this.initChart();
          }
          if(res.code == 20001){
            this.$message.info("没有数据")
          }
        })
    },
    initChart() {
      var option2 = {
        title: {
          text: "负面评论词云图",
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
            data: this.wordData2,
          },
        ],
      };
      var option1 = {
        title: {
          text: "正面评论词云图",
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
            data: this.wordData1,
          },
        ],
      };

      var circleOptioin = {
        title: {
          text: "评论情感属性",
          left: "center",
        },
        tooltip: {
          trigger: "item",
        },
        legend: {
          top: "5%",
          left: "center",
        },
        series: [
          {
            name: "Access From",
            type: "pie",
            radius: ["40%", "70%"],
            avoidLabelOverlap: false,
            label: {
              show: false,
              position: "center",
            },
            emphasis: {
              label: {
                show: true,
                fontSize: "40",
                fontWeight: "bold",
              },
            },
            labelLine: {
              show: false,
            },
            data: [
              { value: this.po_count, name: "正面评论" },
              { value: this.pa_count, name: "负面评论" },
              { value: this.ne_count, name: "中性评论" },
            ],
          },
        ],
      };
      this.$echarts
        .init(document.getElementById("circle1"))
        .setOption(circleOptioin);
      this.$echarts
        .init(document.getElementById("echarts1"))
        .setOption(option1);
      this.$echarts
        .init(document.getElementById("echarts2"))
        .setOption(option2);
    },
  },
};
</script>

<style>
.container{
    padding:10px;
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
