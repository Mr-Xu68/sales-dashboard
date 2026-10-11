import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="中小企业销售数据看板", page_icon="📈", layout="wide")
st.title("📈 中小企业销售数据自动分析看板")

# ---------- 加载数据 ----------
@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv', parse_dates=['日期'])
    return df

df = load_data()

# ---------- 侧边栏筛选 ----------
st.sidebar.header("筛选条件")
selected_regions = st.sidebar.multiselect(
    "选择地区", options=df['区域'].unique(), default=df['区域'].unique()
)
selected_products = st.sidebar.multiselect(
    "选择产品", options=df['产品'].unique(), default=df['产品'].unique()
)
date_range = st.sidebar.date_input(
    "日期范围", value=[df['日期'].min(), df['日期'].max()]
)

# 应用筛选
mask = (
    df['区域'].isin(selected_regions) &
    df['产品'].isin(selected_products) &
    (df['日期'] >= pd.to_datetime(date_range[0])) &
    (df['日期'] <= pd.to_datetime(date_range[1]))
)
filtered = df[mask]

# ---------- KPI 指标卡 ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("总销售额", f"¥{filtered['销售额'].sum():,.0f}")
col2.metric("总销量", f"{filtered['销售量'].sum():,}")
col3.metric("平均单价", f"¥{filtered['单价'].mean():.2f}")
col4.metric("订单数", f"{len(filtered):,}")

st.divider()

# ---------- 销售额趋势 ----------
st.subheader("📅 销售额趋势")
trend = filtered.groupby('日期')['销售额'].sum().reset_index()
trend['7日移动平均'] = trend['销售额'].rolling(window=7, min_periods=1).mean()

fig_trend = px.line(
    trend, x='日期',
    y=['销售额', '7日移动平均'],
    title="每日销售额趋势（含7日移动平均）",
    color_discrete_map={'销售额': '#4C78A8', '7日移动平均': '#F58518'},
    labels={'value': '销售额（元）', 'variable': '指标'},
)
fig_trend.update_traces(line=dict(width=2.5))
fig_trend.update_traces(line=dict(dash='dash'), selector=dict(name='7日移动平均'))
fig_trend.update_layout(
    xaxis_title="日期",
    yaxis_title="销售额（元）",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="近7天", step="day", stepmode="backward"),
                dict(count=14, label="近14天", step="day", stepmode="backward"),
                dict(count=30, label="近30天", step="day", stepmode="backward"),
                dict(label="全部", step="all"),
            ])
        ),
        rangeslider=dict(visible=True, thickness=0.08),
        type="date",
    ),
    yaxis=dict(tickprefix="¥", tickformat=","),
)
st.plotly_chart(fig_trend, use_container_width=True)

# ---------- 地区销售分布 ----------
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("🗺️ 地区销售分布")
    region_sales = filtered.groupby('区域')['销售额'].sum().reset_index()
    fig_region = px.bar(region_sales, x='区域', y='销售额', color='区域',
                        title="各地区销售额")
    st.plotly_chart(fig_region, use_container_width=True)

with col_right:
    st.subheader("📦 产品销售对比")
    product_sales = filtered.groupby('产品')['销售额'].sum().reset_index()
    fig_product = px.pie(product_sales, names='产品', values='销售额',
                         title="产品销售额占比")
    st.plotly_chart(fig_product, use_container_width=True)

# ---------- 原始数据预览 ----------
with st.expander("查看原始数据"):
    st.dataframe(filtered.head(100))