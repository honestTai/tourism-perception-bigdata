import request from '@/utils/request'

export default {
    recommendData(data){
        return request({
            url: '/data',
            method: 'post',
            data: data
        })
    },
    university(data){
        return request({
            url: '/university',
            method: 'post',
            data: data
        })
    },
    universityParam(data){
        return request({
            url: '/uni_param',
            method: 'post',
            data: data
        })
    },
    relavetiveTopic(data){
        return request({
            url: '/relative',
            method: 'post',
            data: data
        })
    },
    calculateTopic(data){
        return request({
            url: '/topicDetail',
            method: 'post',
            data: data
        })
    },
    suggestTopic(data){
        return request({
            url: '/suggest',
            method: 'post',
            data: data
        })
    },
    recentlyWeek(data){
        return request({
            url: '/recently',
            method: 'post',
            data: data
        })
    },
    getWordCount(data){
        return request({
            url: '/wordCloud',
            method: 'post',
            data: data
        })
    },
    categoryDataForWeek(data){
        return request({
            url: '/category',
            method: 'post',
            data: data
        })
    },
    POPTopicForWeek(data){
        return request({
            url: '/pop',
            method: 'post',
            data: data
        })
    },
    regionData(data){
        return request({
            url: '/region',
            method: 'post',
            data: data
        })
    },
  allComments(data){
    return request({
      url: '/allComments',
      method: 'post',
      data: data
    })
  },
  priceDat(){
    return request({
      url: '/price',
      method: 'GET'
    })
  },
  att(data) {
    return request({
      url: '/att',
      method: 'POST',
      data:data
    })
  },
  attGetAll() {
    return request({
      url: '/attGetAll',
      method: 'GET'
    })
  }
}
