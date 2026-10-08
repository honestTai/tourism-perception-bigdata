import defaultSettings from '@/settings'

const institution=[
  '文学院',
  '语言科学与艺术学院',
  '历史文化与旅游学院',
  '法律政治学院',
  '外国语学院',
  '商学院',
  '教育科学学院（教师教育学院）', 
  '数学与统计学院',
  '物理与电子工程学院', 
  '化学化工学院',
  '生命科学学院',
  '马克思主义学院',
  '体育学院',
  '音乐学院',
  '美术学院',
  '传媒与影视学院',
  '计算机科学与技术学院（智慧教育学院）', 
  '机电工程学院',
  '中俄学院',
  '电气工程及自动化学院',
  '地理测绘与城乡规划学院',
  '科文学院',
  '敬文书院',
  '圣彼得堡彼得大帝理工大学联合工程学院',
  '健康科学学院'
  ]

  const ReservationStatus = [
    {'id':0,'desc':'预约中'},
    {'id':1,'desc':'等待签到'},
    {'id':2,'desc':'签到完成'},
    {'id':3,'desc':'审核通过'},
    {'id':404,'desc':'无效的'}
  ]

  const RoomStatus = [
    {'id':1,'desc':'可以使用'},
    {'id':0,'desc':'禁止使用'},
    {'id':2,'desc':'正在使用中'}
  ]

  const RoomUsage = [
    {'id':1,'desc':'活动'},
    {'id':2,'desc':'自习'},
    {'id':3,'desc':'课程'}
  ]

  const ApplyStatus = [
    {'id':1,'desc':'申请中'},
    {'id':2,'desc':'申请通过'}
  ]

export default {
    institution,
    ReservationStatus,
    RoomStatus,
    RoomUsage
}

