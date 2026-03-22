import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from PIL import Image
import os
import matplotlib.font_manager as fm

# 配置页面
st.set_page_config(
    page_title="世界·永康五金指数 - 智能决策平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 隐藏 Streamlit 默认的菜单和 footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 侧边栏导航
# ==========================================
st.sidebar.title("📈 永康五金指数")
st.sidebar.markdown("### 智能决策赋能平台")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "功能导航",
    (
        "📊 平台总览 (Dashboard)", 
        "🔍 宏观行业洞察 (Macro)", 
        "⚠️ 风险预警雷达 (Risk)", 
        "🧩 SaaS模块推荐 (SaaS)", 
        "🌐 产业生态网络 (SNA)",
        "🎯 潜在客户画像 (CRM)"
    )
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**关于平台**\n\n"
    "本平台基于海量宏观时间序列数据，"
    "利用 RSF、Apriori、SNA、K-Modes 等算法，"
    "实现从“宏观监测”向“微观赋能”的战略转型。"
)

# 辅助函数：加载图片
def load_image(image_name):
    # 针对 GitHub 部署，图片和 app.py 放在同级目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, image_name)
    if os.path.exists(path):
        return Image.open(path)
    return None

# ==========================================
# 页面路由逻辑
# ==========================================

if menu == "📊 平台总览 (Dashboard)":
    st.title("🌟 世界·永康五金指数 - 智能决策平台")
    st.markdown("### 欢迎使用新一代数据赋能系统")
    st.markdown("""
    本平台旨在打破传统宏观数据“只能看不能用”的瓶颈，通过深度挖掘五金产业数据，为中小企业提供**主动式的风险预警**和**定制化的业务指导**。
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("监控行业数", "8 个", "覆盖核心五金分类")
    col2.metric("核心监测维度", "5 大维度", "景气、价格、电商、创新、物流")
    col3.metric("预测准确率提升", "+198.4%", "基于RSF算法")
    col4.metric("高价值客户占比", "32.29%", "核心优质客户")
    
    st.markdown("---")
    st.subheader("平台核心功能架构")
    
    c1, c2 = st.columns(2)
    with c1:
        st.info("#### 1. 宏观洞察与预警\n实时监控八大行业的价格、景气度波动，智能诊断内外贸利润剪刀差，提前规避产业风险。")
        st.success("#### 2. SaaS 智能推荐\n基于 Apriori 算法，挖掘企业在不同场景下的关联需求，提供精准的模块化数据服务套餐。")
    with c2:
        st.warning("#### 3. 客户画像与分层\n利用 K-Modes 聚类，将海量客户划分为五大类，帮助平台实现精准营销与资源倾斜。")
        st.error("#### 4. 生态网络定位\n通过 SNA 社会网络分析，明确平台在数据、资金、物流交汇中的核心枢纽地位。")

elif menu == "🔍 宏观行业洞察 (Macro)":
    st.title("🔍 宏观行业洞察")
    st.markdown("全景展示永康五金八大行业的市场表现与核心指标相关性。")
    
    tab1, tab2, tab3 = st.tabs(["价格时序走势", "生产景气度分布", "指标相关性矩阵"])
    
    with tab1:
        st.subheader("市场交易价格指数走势监控")
        img = load_image("Chart_1_价格指数时序走势.png")
        if img: st.image(img, use_column_width=True)
        else: st.warning("图片未找到，请确保已运行数据生成脚本。")
        st.markdown("**洞察**：监控发现不同行业的波动周期存在显著差异。部分行业表现出较强的价格韧性，而部分行业在特定时期出现大幅下跌，提示可能进入价格战阶段。")
        
    with tab2:
        st.subheader("八大行业生产景气度诊断")
        img = load_image("Chart_2_生产景气度箱线图.png")
        if img: st.image(img, use_column_width=True)
        st.markdown("**洞察**：“门业”与“休闲器具”的景气分布集中，生产稳定性强；“技术装备”行业离群点较多，受突发性订单驱动明显。")
        
    with tab3:
        st.subheader("宏观指数体系特征交叉相关性")
        img = load_image("Chart_3_指数相关性热力图.png")
        if img: st.image(img, use_column_width=True)
        st.markdown("**洞察**：“外贸价格指数”与“市场景气度”强正相关；“创新指数”与“物流指数”呈负相关，警示高端化转型初期的供应链阵痛。")

elif menu == "⚠️ 风险预警雷达 (Risk)":
    st.title("⚠️ 风险预警与抗风险评估")
    
    # 增加交互：选择行业查看特定预警阈值
    st.markdown("### 🎯 行业自定义风险预警监控")
    selected_industry = st.selectbox(
        "选择您关注的五金细分行业：",
        ["车业", "门业", "杯业", "电动工具", "电器厨具", "休闲器具", "技术装备", "金属材料"]
    )
    
    # 模拟数据反馈
    risk_data = {
        "车业": {"profit_margin": "12.5%", "status": "✅ 健康", "advice": "保持创新投入，巩固电商优势。"},
        "门业": {"profit_margin": "8.2%", "status": "✅ 稳定", "advice": "生产景气度高，建议优化物流成本。"},
        "杯业": {"profit_margin": "-1.5%", "status": "🚨 高危", "advice": "面临价格战风险，急需降本增效工具介入。"},
        "电动工具": {"profit_margin": "6.0%", "status": "⚠️ 预警", "advice": "关注外贸汇率波动与原材料价格。"},
        "电器厨具": {"profit_margin": "7.5%", "status": "✅ 稳定", "advice": "平稳发展，建议探索智能家居转型。"},
        "休闲器具": {"profit_margin": "9.1%", "status": "✅ 健康", "advice": "订单充足，需防范产能过剩。"},
        "技术装备": {"profit_margin": "15.0%", "status": "✅ 健康", "advice": "高附加值，受大宗订单影响大，建议引入定制化风控。"},
        "金属材料": {"profit_margin": "3.5%", "status": "⚠️ 预警", "advice": "受上游大宗商品价格影响剧烈，强烈建议订阅价格预警模块。"}
    }
    
    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.metric("当前行业", selected_industry)
    r_col2.metric("预估平均利润率", risk_data[selected_industry]["profit_margin"])
    
    if "健康" in risk_data[selected_industry]["status"] or "稳定" in risk_data[selected_industry]["status"]:
        r_col3.success(f"系统状态：{risk_data[selected_industry]['status']}")
    elif "预警" in risk_data[selected_industry]["status"]:
        r_col3.warning(f"系统状态：{risk_data[selected_industry]['status']}")
    else:
        r_col3.error(f"系统状态：{risk_data[selected_industry]['status']}")
        
    st.info(f"💡 **AI 赋能建议**：{risk_data[selected_industry]['advice']}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("内外贸利润剪刀差预警")
        img = load_image("Chart_4_内外贸剪刀差.png")
        if img: st.image(img, use_column_width=True)
        st.markdown("**洞察**：动态对比外贸成交价与生产成本价。当外贸价格向下穿透成本线时，系统自动触发行业利润枯竭预警。")
        
    with col2:
        st.subheader("微观抗风险能力对标 (雷达图)")
        img = load_image("Chart_5_行业评价雷达图.png")
        if img: st.image(img, use_column_width=True)
        st.markdown("**洞察**：直观对比不同行业在景气、电商、创新、物流等多维度的短板，为精准帮扶提供依据。")
        
    st.markdown("---")
    st.subheader("基于 RSF 模型的用户生命周期预测")
    c1, c2 = st.columns(2)
    with c1:
        img = load_image("Chart_6_RSF用户留存分析.png")
        if img: st.image(img, use_column_width=True)
    with c2:
        img = load_image("Chart_7_2_RSF部分依赖图.png")
        if img: st.image(img, use_column_width=True)
    st.info("引入主动风控模型后，用户生存期中位数从 6.2 个月提升至 18.5 个月。**数据更新及时性**是影响留存的最关键因素。")

elif menu == "🧩 SaaS模块推荐 (SaaS)":
    st.title("🧩 SaaS微观需求智能推荐")
    st.markdown("基于 Apriori 关联规则挖掘，揭示企业级功能模块之间的强协同效应。")
    
    # 增加交互：模拟 SaaS 购物车推荐
    st.markdown("### 🛒 智能打包推荐模拟器")
    st.write("请选择您企业目前最想开通的一项基础服务，AI 将自动为您推荐协同度最高的高级模块：")
    
    selected_service = st.radio(
        "选择基础服务：",
        ("原材料价格预警", "智能报价参谋", "全球采购商画像", "竞品追踪情报"),
        horizontal=True
    )
    
    recommendation_map = {
        "原材料价格预警": [("智能报价参谋", "4.5", "0.72", "⭐⭐⭐⭐⭐"), ("优企供应链信贷", "2.9", "0.45", "⭐⭐⭐")],
        "智能报价参谋": [("竞品追踪情报", "3.8", "0.65", "⭐⭐⭐⭐")],
        "全球采购商画像": [("海关准入报告", "4.1", "0.68", "⭐⭐⭐⭐⭐")],
        "竞品追踪情报": [("全球采购商画像", "3.2", "0.52", "⭐⭐⭐")]
    }
    
    recs = recommendation_map.get(selected_service, [])
    st.write(f"**基于数万家企业的行为数据，为您生成的交叉销售推荐：**")
    for rec in recs:
        st.success(f"🚀 **强烈推荐搭配**：**[{rec[0]}]**  \n*协同提升度 (Lift)*: {rec[1]} | *转化置信度*: {rec[2]} | *推荐指数*: {rec[3]}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("功能模块感知效用分布")
        img = load_image("Chart_8_联合分析效用分布.png")
        if img: st.image(img, use_column_width=True)
        st.markdown("**商业模式创新**：“定制化风控模型”具有最高感知效用，而昂贵的包年套餐呈负效用，支撑了“按需付费”策略。")
        
    with col2:
        st.subheader("SaaS 需求强关联网络拓扑")
        img = load_image("Chart_9_Apriori网络拓扑.png")
        if img: st.image(img, use_column_width=True)
        st.markdown("**交叉销售策略**：如购买[价格预警]的用户，极大概率需要[报价参谋]（Lift=4.5），系统将自动打包推荐。")

    st.markdown("---")
    st.subheader("关联规则质量分布矩阵")
    img = load_image("Chart_9_2_Apriori规则分布.png")
    if img: 
        # 控制图片显示大小居中
        col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
        with col_c2:
            st.image(img, use_column_width=True)

elif menu == "🌐 产业生态网络 (SNA)":
    st.title("🌐 产业生态网络控制力分析")
    st.markdown("运用社会网络分析 (SNA)，量化评估平台在五金产业链数据流转中的枢纽地位。")
    
    tab1, tab2 = st.tabs(["核心节点控制力 (散点图)", "生态社区发现与拓扑分层"])
    
    with tab1:
        img = load_image("Chart_10_SNA生态节点控制力.png")
        if img: st.image(img, use_column_width=True)
        st.markdown("""
        **度中心性**：衡量节点交互的广泛度。
        **中介中心性**：衡量控制资源流动、作为桥梁的能力。
        数据监测平台双指标均位列第一，证实了其作为产业“神经中枢”的基础。
        """)
        
    with tab2:
        img = load_image("Chart_10_2_SNA社区发现.png")
        if img: st.image(img, use_column_width=True)
        st.markdown("网络整体密度良好。平台与政府海关数据端构成**核心赋能层**，通过银行与物流巨头（**资源支撑层**），最终服务于广大的中小企业（**业务应用层**）。")

elif menu == "🎯 潜在客户画像 (CRM)":
    st.title("🎯 潜在客户分层与精准营销")
    st.markdown("基于 K-Modes 聚类算法，将五金行业的潜在客户划分为五大高价值群体。")
    
    # 增加交互：输入企业特征，AI判定客户群
    st.markdown("### 🔍 客户分群 AI 诊断测试")
    st.write("滑动下方滑块，模拟一家潜在企业的指标表现，系统将实时判断其所属客群。")
    
    slider_col1, slider_col2, slider_col3 = st.columns(3)
    with slider_col1:
        sim_market = st.slider("市场景气指数", 80.0, 100.0, 93.0, 0.1)
    with slider_col2:
        sim_innov = st.slider("创新能力指数", 110.0, 130.0, 125.0, 0.1)
    with slider_col3:
        sim_logistics = st.slider("物流流转指数", 120.0, 135.0, 132.0, 0.1)
        
    # 简单的模拟判定逻辑
    if sim_market >= 92.0 and sim_innov >= 122.0:
        st.success(f"🤖 **AI 判定结果**：当前输入特征最符合 **[🟢 核心优质客户]**。建议立即安排高级销售跟进！")
    elif sim_logistics >= 130.0 and sim_market < 94.0:
        st.error(f"🤖 **AI 判定结果**：当前输入特征最符合 **[🔴 潜力增长客户]**。建议推介供应链对接服务！")
    elif sim_market >= 94.5:
        st.warning(f"🤖 **AI 判定结果**：当前输入特征最符合 **[🟡 成本敏感客户]**。建议推介低成本标准化工具！")
    elif sim_market < 92.0 and sim_innov < 122.0:
        st.info(f"🤖 **AI 判定结果**：当前输入特征最符合 **[🔵 外贸导向 / 边缘客户]**。")
        
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("创新能力-市场景气 双维画像")
        img = load_image("Chart_11_创新与景气聚类.png")
        if img: st.image(img, use_column_width=True)
        
    with col2:
        st.subheader("电商渗透-物流活跃 双维画像")
        img = load_image("Chart_12_电商与物流聚类.png")
        if img: st.image(img, use_column_width=True)
        
    st.markdown("---")
    st.subheader("客户分层洞察与行动建议")
    
    st.success("**🟢 核心优质客户 (占比 ~25%)**：景气度与创新双高，对高阶数据预警有强需求，是利润贡献的主力。应重点推介高阶定制SaaS。")
    st.error("**🔴 潜力增长客户 (占比 ~25%)**：物流流转快，处于扩张期，对供应链优化数据感兴趣。重点推介物流与供应链对接服务。")
    st.info("**🔵 外贸导向客户 (占比 ~28%)**：以外贸价格为核心关注点，是全球采购商画像功能的精准受众。")
    st.warning("**🟡 成本敏感客户 (占比 ~10%)**：景气度较低，对价格极其敏感。需通过低成本、标准化工具切入。")
    st.markdown("**⚫ 边缘存量客户 (占比 ~10%)**：各项指标低迷，购买意愿弱，应降低主动营销投入成本。")

# 页脚
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>© 2026 世界·永康五金指数调研团队 | 基于 Python & Streamlit 构建</div>", unsafe_allow_html=True)
