import pandas as pd
from matplotlib.font_manager import FontProperties
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from database.config import engine
# 读取评论数据
df = pd.read_sql_query("SELECT * FROM comment where ipLocatedName is not null", con=engine)

# 选择文本特征
text_features = ['ipLocatedName', 'publishTypeTag', 'touristTypeDisplay', 'userNick', 'userMember']

# 合并文本特征
df['combined_text'] = df[text_features].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# TF-IDF向量化
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['combined_text'])

# 标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X.toarray())

# 使用K均值聚类
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)

# 解析地域信息
df['ipLocatedName'] = df['ipLocatedName'].astype(str)
df['region'] = df['ipLocatedName']  # 假设地域信息以逗号分隔，取第一部分作为地域信息

# 计算每个聚类中不同地域的评分占比
cluster_region_scores = df.groupby(['cluster', 'region'])['score'].value_counts(normalize=True).unstack().fillna(0)

# 输出每个聚类的评论数量和评分占比
for cluster in df['cluster'].unique():
    print(f"\nCluster {cluster} - Comment Count: {len(df[df['cluster'] == cluster])}\n")
    print(cluster_region_scores.loc[cluster])

# 绘制散点图
for cluster in df['cluster'].unique():
    cluster_data = df[df['cluster'] == cluster]
    plt.scatter(cluster_data['region'], cluster_data['score'], label=f'Cluster {cluster}')



# 绘制图表
plt.xlabel('address')
plt.ylabel('score')
plt.title('kmsresult')
plt.legend()
plt.show()
