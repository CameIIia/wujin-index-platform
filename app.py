import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from PIL import Image
import os
import matplotlib.font_manager as fm

def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# 配置页面
st.set_page_config(
    page_title="世界·永康五金指数 - 智能决策平台",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 隐藏 Streamlit 默认的菜单和 footer, 并注入苹果高端风格全局 CSS
hide_streamlit_style = """
<style>
/* Apple Style Premium CSS */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', 'San Francisco', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Hide default streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Card Style for glassmorphism */
.glass-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    padding: 24px;
    margin-bottom: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.12);
}

/* Metric styling */
div[data-testid="stMetricValue"] {
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    background: -webkit-linear-gradient(45deg, #007AFF, #5856D6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Button styling */
.stButton > button {
    border-radius: 20px !important;
    border: none !important;
    background: #007AFF !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.5rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px 0 rgba(0,118,255,0.39) !important;
}

.stButton > button:hover {
    background: #0056b3 !important;
    box-shadow: 0 6px 20px rgba(0,118,255,0.23) !important;
    transform: translateY(-2px);
}

/* Alert/Info boxes */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
}

/* Typography */
h1, h2, h3 {
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    color: #1d1d1f !important;
}

/* Animation */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.animated-section {
    animation: slideUp 0.3s ease-out forwards;
}

/* Dark mode tweaks if user system is dark */
@media (prefers-color-scheme: dark) {
    .glass-card {
        background: rgba(30, 30, 30, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3 {
        color: #f5f5f7 !important;
    }
    div[data-testid="stMetricValue"] {
        background: -webkit-linear-gradient(45deg, #0A84FF, #5E5CE6);
        -webkit-background-clip: text;
    }
}
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
        "🚀 主动式智能工作台 (Proactive)",
        "🛍️ 商业化定价与商店 (Store)",
        "🔗 业务流嵌入演示 (Workflow)",
        "💬 行业生态与社区 (Community)",
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
# 页面路由逻辑与状态拦截
# ==========================================

if st.session_state.get('show_payment', False):
    st.markdown("<div class='animated-section'>", unsafe_allow_html=True)
    st.title("💳 支付收银台")
    st.markdown(f"### 订单信息：<span style='color:#007AFF'>{st.session_state.get('payment_item', '')}</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<div style='background-color:#09B83E; color:white; font-size:40px; font-weight:bold; width:80px; height:80px; border-radius:15px; line-height:80px; text-align:center; margin:0 auto; box-shadow: 0 4px 10px rgba(9,184,62,0.3);'>微</div><br>", unsafe_allow_html=True)
        st.markdown("#### 微信支付")
        if st.button("确认支付", key="pay_wechat"):
            st.session_state['show_payment'] = False
            st.session_state['show_success'] = f"支付成功：已为您开通 {st.session_state['payment_item']} 权限！"
            rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<div style='background-color:#1677FF; color:white; font-size:40px; font-weight:bold; width:80px; height:80px; border-radius:15px; line-height:80px; text-align:center; margin:0 auto; box-shadow: 0 4px 10px rgba(22,119,255,0.3);'>支</div><br>", unsafe_allow_html=True)
        st.markdown("#### 支付宝")
        if st.button("确认支付", key="pay_alipay"):
            st.session_state['show_payment'] = False
            st.session_state['show_success'] = f"支付成功：已为您开通 {st.session_state['payment_item']} 权限！"
            rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← 返回订单页", key="btn_cancel_pay"):
        st.session_state['show_payment'] = False
        rerun_app()
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.get('show_app_detail', False):
    st.markdown("<div class='animated-section'>", unsafe_allow_html=True)
    if st.button("← 返回应用商店"):
        st.session_state['show_app_detail'] = False
        rerun_app()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    icon = st.session_state.get('app_detail_icon', '🧩')
    item = st.session_state.get('app_detail_item', '')
    desc = st.session_state.get('app_detail_desc', '')
    price = st.session_state.get('app_detail_price', '')
    
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"<div style='background:linear-gradient(135deg, #f5f7fa 0%, #e4eaf5 100%); border-radius:20px; height:250px; display:flex; align-items:center; justify-content:center; font-size:80px; box-shadow:0 10px 20px rgba(0,0,0,0.05);'>{icon}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"## {item}")
        st.markdown(f"### <span style='color:#007AFF;'>{price}</span>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("#### 应用介绍")
        st.write(desc)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 使用 Streamlit 官方参数 type="primary" 让按钮变蓝高亮
        if st.button("立即购买", key="buy_app_detail", type="primary"):
            st.session_state['show_app_detail'] = False
            st.session_state['show_payment'] = True
            st.session_state['payment_item'] = f"{item} ({price})"
            rerun_app()
            
    st.markdown("---")
    st.markdown("#### 接口展示")
    st.info("💡 此应用已由“世界·永康五金指数”数据中台提供底层接口支持，购买后可自动集成至您的主控面板或通过 API 调用。")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "📊 平台总览 (Dashboard)":
    if st.session_state.get('show_success', ""):
        st.toast(st.session_state['show_success'], icon="🎉")
        st.success(st.session_state['show_success'])
        st.session_state['show_success'] = ""

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
        if img: st.image(img, width="stretch")
        else: st.warning("图片未找到，请确保已运行数据生成脚本。")
        st.markdown("**洞察**：监控发现不同行业的波动周期存在显著差异。部分行业表现出较强的价格韧性，而部分行业在特定时期出现大幅下跌，提示可能进入价格战阶段。")
        
    with tab2:
        st.subheader("八大行业生产景气度诊断")
        img = load_image("Chart_2_生产景气度箱线图.png")
        if img: st.image(img, width="stretch")
        st.markdown("**洞察**：“门业”与“休闲器具”的景气分布集中，生产稳定性强；“技术装备”行业离群点较多，受突发性订单驱动明显。")
        
    with tab3:
        st.subheader("宏观指数体系特征交叉相关性")
        img = load_image("Chart_3_指数相关性热力图.png")
        if img: st.image(img, width="stretch")
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
        if img: st.image(img, width="stretch")
        st.markdown("**洞察**：动态对比外贸成交价与生产成本价。当外贸价格向下穿透成本线时，系统自动触发行业利润枯竭预警。")
        
    with col2:
        st.subheader("微观抗风险能力对标 (雷达图)")
        img = load_image("Chart_5_行业评价雷达图.png")
        if img: st.image(img, width="stretch")
        st.markdown("**洞察**：直观对比不同行业在景气、电商、创新、物流等多维度的短板，为精准帮扶提供依据。")
        
    st.markdown("---")
    st.subheader("基于 RSF 模型的用户生命周期预测")
    c1, c2 = st.columns(2)
    with c1:
        img = load_image("Chart_6_RSF用户留存分析.png")
        if img: st.image(img, width="stretch")
    with c2:
        img = load_image("Chart_7_2_RSF部分依赖图.png")
        if img: st.image(img, width="stretch")
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
        if img: st.image(img, width="stretch")
        st.markdown("**商业模式创新**：“定制化风控模型”具有最高感知效用，而昂贵的包年套餐呈负效用，支撑了“按需付费”策略。")
        
    with col2:
        st.subheader("SaaS 需求强关联网络拓扑")
        img = load_image("Chart_9_Apriori网络拓扑.png")
        if img: st.image(img, width="stretch")
        st.markdown("**交叉销售策略**：如购买[价格预警]的用户，极大概率需要[报价参谋]（Lift=4.5），系统将自动打包推荐。")

    st.markdown("---")
    st.subheader("关联规则质量分布矩阵")
    img = load_image("Chart_9_2_Apriori规则分布.png")
    if img: 
        # 控制图片显示大小居中
        col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
        with col_c2:
            st.image(img, width="stretch")

elif menu == "🌐 产业生态网络 (SNA)":
    st.title("🌐 产业生态网络控制力分析")
    st.markdown("运用社会网络分析 (SNA)，量化评估平台在五金产业链数据流转中的枢纽地位。")
    
    tab1, tab2 = st.tabs(["核心节点控制力 (散点图)", "生态社区发现与拓扑分层"])
    
    with tab1:
        img = load_image("Chart_10_SNA生态节点控制力.png")
        if img: st.image(img, width="stretch")
        st.markdown("""
        **度中心性**：衡量节点交互的广泛度。
        **中介中心性**：衡量控制资源流动、作为桥梁的能力。
        数据监测平台双指标均位列第一，证实了其作为产业“神经中枢”的基础。
        """)
        
    with tab2:
        img = load_image("Chart_10_2_SNA社区发现.png")
        if img: st.image(img, width="stretch")
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
        if img: st.image(img, use_container_width=True)
        
    with col2:
        st.subheader("电商渗透-物流活跃 双维画像")
        img = load_image("Chart_12_电商与物流聚类.png")
        if img: st.image(img, use_container_width=True)
        
    st.markdown("---")
    st.subheader("客户分层洞察与行动建议")
    
    st.success("**🟢 核心优质客户 (占比 ~25%)**：景气度与创新双高，对高阶数据预警有强需求，是利润贡献的主力。应重点推介高阶定制SaaS。")
    st.error("**🔴 潜力增长客户 (占比 ~25%)**：物流流转快，处于扩张期，对供应链优化数据感兴趣。重点推介物流与供应链对接服务。")
    st.info("**🔵 外贸导向客户 (占比 ~28%)**：以外贸价格为核心关注点，是全球采购商画像功能的精准受众。")
    st.warning("**🟡 成本敏感客户 (占比 ~10%)**：景气度较低，对价格极其敏感。需通过低成本、标准化工具切入。")
    st.markdown("**⚫ 边缘存量客户 (占比 ~10%)**：各项指标低迷，购买意愿弱，应降低主动营销投入成本。")

# ==========================================
# 新增落地展示模块 (紧扣企业命题)
# ==========================================

elif menu == "🚀 主动式智能工作台 (Proactive)":
    st.markdown("<div class='animated-section'>", unsafe_allow_html=True)
    st.title("🚀 主动式智能工作台")
    st.markdown("将复杂指数转化为**一句话业务建议**，告别被动查询，实现数据找人。解决中小企业“能力不匹配”的核心痛点。")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔔 今日核心推送 (Based on RSF Model)")
    c1, c2 = st.columns([1, 6])
    c1.image("https://img.icons8.com/color/96/000000/appointment-reminders--v1.png", width=60)
    c2.markdown("#### [铜材价格异动预警]\n**昨日国际铜价跌幅超 4.2%**。建议门业、杯业客户暂缓长期采购合约，转为现货采买。")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📈 您的商机雷达")
        st.success("🎯 **采购建议**：不锈钢主连下行，建议备货率提升至 45%。")
        st.info("💡 **市场风向**：中东地区“休闲器具”检索量激增 120%。")
        st.warning("⚠️ **库存预警**：您的核心竞品平均去库周期缩短 3 天。")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("查看详细情报", key="btn_radar"):
            st.toast("已为您生成深度情报报告！正在后台推送...", icon="🔍")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ 自动化执行流")
        st.checkbox("当原材料下降 5% 时，自动触发采购审批流", value=True)
        st.checkbox("当行业景气度低于 90 时，自动冻结营销预算扩增", value=False)
        st.checkbox("每周五生成定制化周报发送至钉钉/微信", value=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("保存工作流", key="btn_workflow"):
            st.toast("工作流已成功保存并激活！自动化引擎已接管。", icon="✅")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🛍️ 商业化定价与商店 (Store)":
    st.markdown("<div class='animated-section'>", unsafe_allow_html=True)
    st.title("🛍️ 商业化定价与数据应用商店")
    st.markdown("探索多元盈利模式：从单一卖数据，向提供 **SaaS 微服务、深度报告与自动化工具** 转型。解决平台“价值模糊”与“付费意愿低”的问题。")
    
    st.subheader("💎 平台订阅方案")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div class='glass-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("## 免费版\n### ¥0 / 月")
        st.markdown("---")
        st.markdown("✔️ 基础价格指数浏览<br>✔️ 宏观景气度查询<br>✔️ 每月 1 次简易分析<br><span style='color: #ccc'>❌ 主动预警推送</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("当前版本", disabled=True, key="btn_free")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c2:
        st.markdown("<div class='glass-card' style='text-align: center; border: 2px solid #007AFF; transform: scale(1.05);'>", unsafe_allow_html=True)
        st.markdown("## 专业版 👑\n### ¥299 / 月")
        st.markdown("---")
        st.markdown("✔️ **所有基础版功能**<br>✔️ **短信/微信异动预警**<br>✔️ **每月 5 份深度洞察报告**<br>✔️ 行业生态图谱解锁", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("立即升级", key="btn_pro"):
            st.session_state['show_payment'] = True
            st.session_state['payment_item'] = "专业版 👑 (¥299/月)"
            rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with c3:
        st.markdown("<div class='glass-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.markdown("## 企业版\n### 需咨询")
        st.markdown("---")
        st.markdown("✔️ **所有专业版功能**<br>✔️ **API 接口对接 (ERP集成)**<br>✔️ 定制化风控模型部署<br>✔️ 1v1 专家咨询服务", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("联系销售", key="btn_ent"):
            st.toast("专属销售代表（工号882）已收到提醒，将在 3 分钟内与您联系！", icon="📞")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧩 增值微应用商店 (按需购买)")
    sc1, sc2, sc3 = st.columns(3)
    
    with sc1:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.info("🛠️ **智能报价器插件**")
        st.markdown("结合实时指数，自动生成外贸最优报价单。<br><br>**¥9.9 / 次**", unsafe_allow_html=True)
        if st.button("查看详情", key="app1"):
            st.session_state['show_app_detail'] = True
            st.session_state['app_detail_item'] = "智能报价器插件"
            st.session_state['app_detail_price'] = "¥9.9 / 次"
            st.session_state['app_detail_desc'] = "通过对接五金指数实时价格库，为您的每一笔外贸订单自动测算成本底线，并在利润空间允许的前提下，生成最优的阶梯报价单，极大提升业务员的谈判底气与利润率。"
            st.session_state['app_detail_icon'] = "🛠️"
            rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sc2:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.success("📦 **海关买家画像包**")
        st.markdown("解锁特定区域买家的采购频次与偏好。<br><br>**¥199 / 份**", unsafe_allow_html=True)
        if st.button("查看详情", key="app2"):
            st.session_state['show_app_detail'] = True
            st.session_state['app_detail_item'] = "海关买家画像包"
            st.session_state['app_detail_price'] = "¥199 / 份"
            st.session_state['app_detail_desc'] = "基于脱敏的跨境物流和海关提单数据，为您深度剖析指定海外采购商的历史采购频次、偏好品类、平均单价，帮您在开发新客户、发送开发信时做到知己知彼。"
            st.session_state['app_detail_icon'] = "📦"
            rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sc3:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.warning("📊 **竞品产能监测器**")
        st.markdown("利用卫星与物流数据估算竞品生产动态。<br><br>**¥399 / 月**", unsafe_allow_html=True)
        if st.button("查看详情", key="app3"):
            st.session_state['show_app_detail'] = True
            st.session_state['app_detail_item'] = "竞品产能监测器"
            st.session_state['app_detail_price'] = "¥399 / 月"
            st.session_state['app_detail_desc'] = "运用多源数据交叉验证技术（涵盖竞品工厂所在园区的物流重卡出入频次、区域耗电量波动等），为您动态推算核心竞争对手的当前产能负荷与开工率，助力您的战略排期和价格战准备。"
            st.session_state['app_detail_icon'] = "📊"
            rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🔗 业务流嵌入演示 (Workflow)":
    st.markdown("<div class='animated-section'>", unsafe_allow_html=True)
    st.title("🔗 业务流无缝嵌入 (API / Widget)")
    st.markdown("解决数据“孤立化”问题，让五金指数直接长在企业自己的办公系统里。")
    
    st.markdown("### 💻 场景演示：企业内部的 [智能报价录入系统]")
    st.markdown("<div class='glass-card' style='background: rgba(248, 249, 250, 0.8); border: 1px solid rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
    
    st.markdown("#### 新建销售报价单")
    wc1, wc2 = st.columns([1.5, 1])
    
    with wc1:
        st.text_input("客户名称", "迪拜 Al-Futtaim 五金批发商")
        st.text_input("产品品类", "高端防盗门")
        st.number_input("拟报单价 (USD)", value=125.0)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 生成最终报价单"):
            st.toast("报价单已生成，并自动附加了永康五金指数背书凭证！", icon="📄")
        
    with wc2:
        st.markdown("<div style='background: rgba(255,255,255,0.9); padding: 20px; border-radius: 12px; border-left: 5px solid #007AFF; box-shadow: 0 4px 15px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
        st.markdown("##### 📈 永康指数 - 报价参谋插件")
        st.metric("防盗门外贸景气度", "98.2", "↑ 2.1% (适宜提价)")
        st.metric("主材(冷轧板)均价", "4200元/吨", "↓ 1.5% (成本下降)")
        st.markdown("**AI 建议**：当前外贸需求旺盛且成本下行。建议您的报价可**上浮 3%-5%**，预计不影响成交率。")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    st.info("💡 **商业价值**：通过 API 接口，五金指数化身为无处不在的“决策幽灵”，极大地提高了系统不可替代性。")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "💬 行业生态与社区 (Community)":
    st.markdown("<div class='animated-section'>", unsafe_allow_html=True)
    st.title("💬 行业生态与专家智库")
    st.markdown("打造包含供应商、经销商、专家在内的生态圈，用“人”的连接解决平台黏性问题。")
    
    tab_com1, tab_com2 = st.tabs(["🔥 圈子动态", "👨‍🏫 专家1v1问答"])
    
    with tab_com1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📝 行业头条")
        st.markdown("👤 **王总 (某头部杯业集团)**： *“刚根据平台的原材料预警，锁定了下半年的不锈钢材，感谢指数平台！大家最近外贸订单如何？”* <br><span style='color: gray; font-size: 0.8em;'>2小时前 · 12 条回复 · 45 赞同</span>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("👤 **数据分析师-李工**： *“发布了深度报告《中东市场休闲器具趋势预测》，欢迎大家在商城下载交流。”* <br><span style='color: gray; font-size: 0.8em;'>5小时前 · 8 条回复 · 112 赞同</span>", unsafe_allow_html=True)
        st.text_input("分享您的行业见解...", key="post_input")
        if st.button("发布动态", key="post_btn"):
            st.toast("动态发布成功！正在等待行业审核...", icon="🚀")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_com2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 🏆 驻场专家面对面")
        e1, e2, e3 = st.columns(3)
        with e1:
            st.image("https://img.icons8.com/color/96/000000/manager.png", width=60)
            st.markdown("**张教授**\n\n供应链管理专家")
            if st.button("向TA提问 (¥50)", key="ask1"):
                st.session_state['show_payment'] = True
                st.session_state['payment_item'] = "向 张教授 提问 (¥50)"
                rerun_app()
        with e2:
            st.image("https://img.icons8.com/color/96/000000/businesswoman.png", width=60)
            st.markdown("**刘总监**\n\n资深大宗商品分析师")
            if st.button("向TA提问 (¥80)", key="ask2"):
                st.session_state['show_payment'] = True
                st.session_state['payment_item'] = "向 刘总监 提问 (¥80)"
                rerun_app()
        with e3:
            st.image("https://img.icons8.com/color/96/000000/engineer.png", width=60)
            st.markdown("**赵工**\n\n五金生产数字化架构师")
            if st.button("向TA提问 (¥60)", key="ask3"):
                st.session_state['show_payment'] = True
                st.session_state['payment_item'] = "向 赵工 提问 (¥60)"
                rerun_app()
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>© 2026 世界·永康五金指数调研团队 | 基于 Python & Streamlit 构建</div>", unsafe_allow_html=True)
