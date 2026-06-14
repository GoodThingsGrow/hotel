import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==========================================
# 1. 页面配置与标题
# ==========================================
st.set_page_config(page_title="Ivan Hotel DRM Dashboard", layout="wide", page_icon="🍸")
st.title("🍸 Ivan Hotel | 收益管理驾驶舱 (DRM Dashboard)")
st.markdown("---")

# 创建三标签页
# 修改顶部的标签页声明 (替换原来的 st.tabs 这一行)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 业务大盘 (Overview)", 
    "🏥 综合健康度监测 (Health Monitor)", 
    "🔬 异动归因分析 (Variance Attribution)",
    "💰 净利润与渠道获客成本 (Net RevPAR)",
    "🍽️ 全面收益管理 (Total Revenue/TrevPAR)"
])

# ==========================================
# 2. 标签页 1: 业务大盘 (保留原有的基础概览)
# ==========================================
with tab1:
    TOTAL_ROOMS = 557
    
    st.subheader("今日核心业务表现")
    kpi_data = {
        "指标": ["入住率 (Occ %)", "平均房价 (ADR) HKD", "单房收益 (RevPAR) HKD", "总客房收益 HKD"],
        "今日实际": ["86.5%", "1,850", "1,600", "891,375"],
        "对比预算": ["+2.1%", "-50", "+30", "+16,710"],
        "同比去年 (YoY)": ["+5.0%", "+120", "+185", "+103,045"]
    }
    cols = st.columns(4)
    for i, col in enumerate(cols):
        col.metric(label=kpi_data["指标"][i], value=kpi_data["今日实际"][i], delta=kpi_data["对比预算"][i])
    
    col1_1, col1_2 = st.columns(2)
    with col1_1:
        st.write("📈 未来14天预订趋势 (Booking Pace)")
        dates = [(datetime.today() + timedelta(days=i)).strftime('%m-%d') for i in range(14)]
        otb = np.random.randint(200, 500, 14)
        forecast = otb + np.random.randint(50, 150, 14)
        pace_df = pd.DataFrame({'日期': dates, 'OTB': otb, '预计增量': forecast - otb})
        
        fig_pace = go.Figure()
        fig_pace.add_trace(go.Bar(x=pace_df['日期'], y=pace_df['OTB'], name='OTB', marker_color='#8e44ad'))
        fig_pace.add_trace(go.Bar(x=pace_df['日期'], y=pace_df['预计增量'], name='预计增量', marker_color='#d7bde2'))
        fig_pace.add_trace(go.Scatter(x=pace_df['日期'], y=[TOTAL_ROOMS]*14, mode='lines', name='满房线', line=dict(color='red', dash='dash')))
        fig_pace.update_layout(barmode='stack', hovermode='x unified', margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_pace, use_container_width=True)

    with col1_2:
        st.write("🏆 竞争群对标 (STAR Report - RevPAR Index)")
        comp_set = ['Ivan Hotel', 'St. Regis', 'Morpheus', 'Ritz-Carlton', 'Banyan Tree']
        revpar_index = [112, 125, 108, 135, 105]
        star_df = pd.DataFrame({'酒店': comp_set, 'ARI': revpar_index})
        fig_star = px.bar(star_df, x='酒店', y='ARI', text='ARI', color='酒店', color_discrete_sequence=['#ff007f'] + ['#bdc3c7']*4)
        fig_star.add_hline(y=100, line_dash="dash", line_color="black")
        fig_star.update_layout(showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_star, use_container_width=True)

# ==========================================
# 3. 标签页 2: 综合健康度监测 (新增深度分析)
# ==========================================
with tab2:
    st.markdown("### 1. 🚨 价格与渠道健康度 (Price Parity & Channel Health)")
    st.caption("监测全网渠道价格倒挂风险及价格规则执行情况")
    
    # 模拟价格监测数据
    parity_data = pd.DataFrame({
        "渠道": ["Booking.com", "Agoda", "携程 (Ctrip)", "飞猪 (Fliggy)", "批发商 A", "Marriott App (基准)"],
        "基础房型售价 (HKD)": [1850, 1780, 1850, 1800, 1600, 1850],
        "状态": ["✅ 正常", "❌ 倒挂危险", "✅ 正常", "⚠️ 轻微倒挂", "❌ 违规上线C端", "🔵 基准价"],
        "当前限制规则": ["无", "连住2晚", "无", "无", "黑出期 (Blackout)", "无"]
    })
    
    def color_status(val):
        color = 'red' if '❌' in val else 'orange' if '⚠️' in val else 'green' if '✅' in val else 'blue'
        return f'color: {color}; font-weight: bold'
    
    st.dataframe(parity_data.style.map(color_status, subset=['状态']), use_container_width=True)

    st.markdown("---")
    
    col2_1, col2_2 = st.columns(2)
    
    with col2_1:
        st.markdown("### 2. ⏱️ 平均入住时长与住客画像 (LOS & Segment Health)")
        # 模拟停留时长和住客画像数据
        segments = ['散客 (Retail)', '会员 (Marriott Bonvoy)', '公司客 (Corporate)', '会议团队 (MICE)', '套餐/长住 (Package)']
        avg_los = [1.2, 1.8, 2.5, 3.1, 4.0]
        adr_by_seg = [2200, 1950, 1600, 1500, 1400]
        
        fig_los = go.Figure()
        fig_los.add_trace(go.Bar(x=segments, y=avg_los, name='平均停留晚数 (LOS)', marker_color='#3498db', yaxis='y1'))
        fig_los.add_trace(go.Scatter(x=segments, y=adr_by_seg, name='平均房价 (ADR)', mode='lines+markers', marker_color='#e74c3c', yaxis='y2'))
        
        fig_los.update_layout(
            yaxis=dict(title='晚数 (Nights)', side='left'),
            yaxis2=dict(title='HKD', side='right', overlaying='y', showgrid=False),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_los, use_container_width=True)
        st.caption("🔍 **DRM 洞察**：散客 LOS 仅 1.2 晚，周末周转成本极高。建议在旺季周末对 Retail 强制设置 **Min LOS 2 (最低连住2晚)** 限制。")

    with col2_2:
        st.markdown("### 3. 🛏️ 房型库存健康度 (Room Type Inventory Health)")
        # 模拟各房型出租率 (反映升级压力)
        room_types = ['奇妙客房 (基础)', '壮美客房', '酷角客房', '非凡套房', '惊喜套房']
        total_inv = [300, 150, 60, 40, 7]
        sold_inv = [295, 120, 30, 10, 1]
        occ_pct = [round(s/t*100, 1) for s, t in zip(sold_inv, total_inv)]
        
        fig_inv = go.Figure(go.Bar(
            x=occ_pct, y=room_types, orientation='h',
            marker=dict(color=occ_pct, colorscale='RdYlGn_r'),
            text=[f"{p}% ({s}/{t})" for p, s, t in zip(occ_pct, sold_inv, total_inv)],
            textposition='auto'
        ))
        fig_inv.update_layout(xaxis_title="出租率 (%)", margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_inv, use_container_width=True)
        st.caption("🔍 **DRM 洞察**：基础房型濒临超售 (98.3%)，而高级套房严重滞销。应立即：1. 提高基础房型价格；2. 向基础房预订客推送付费升级优惠 (eStandby Upgrade)。")

    st.markdown("---")

    st.markdown("### 4. 📅 特定关键日期 OTB 监控 (Special Event OTB Health)")
    # 比如未来某个周六有大型演唱会
    event_date = st.date_input("选择监测日期 (例如：未来大型演唱会/节假日)", datetime.today() + timedelta(days=30))
    
    col_e1, col_e2, col_e3 = st.columns(3)
    with col_e1:
        st.metric(label=f"OTB 出租率进度 vs 目标", value="65%", delta="-10% (进度落后)", delta_color="inverse")
    with col_e2:
        st.metric(label=f"当前上账 ADR vs 去年同期", value="HKD 2,850", delta="+HKD 350")
    with col_e3:
        st.metric(label=f"过去 7 天净新增预订 (Pickup)", value="12 间", delta="-5 间 (流速放缓)", delta_color="inverse")
        
    st.warning(f"**健康度告警 ({event_date.strftime('%Y-%m-%d')})**：价格同比提升过高导致预订流速（Pickup）显著放缓，OTB 进度落后于历史曲线（Booking Curve）。建议：暂缓涨价，针对特定忠诚度会员释放限定促销，刺激基础盘。")


# ==========================================
# 4. 标签页 3: 异动归因分析 (新增核心硬核板块)
# ==========================================
with tab3:
    st.markdown("### 1. 宏观营收异动拆解 (Total RevPAR Variance Breakdown)")
    st.caption("分析相比去年同期 (YoY) 的 RevPAR 增长，是由房价驱动还是入住率驱动？")
    
    # --- 模拟归因计算数据 ---
    # 去年同期 (LY): Occ = 81.5%, ADR = 1730 -> RevPAR = 1410
    # 今日实际 (TY): Occ = 86.5%, ADR = 1850 -> RevPAR = 1600
    occ_ly, adr_ly = 0.815, 1730
    occ_ty, adr_ty = 0.865, 1850
    
    # 计算各项归因贡献度 (应用加法、乘法分解逻辑)
    vol_effect = (occ_ty - occ_ly) * adr_ly
    rate_effect = (adr_ty - adr_ly) * occ_ly
    mix_effect = (occ_ty - occ_ly) * (adr_ty - adr_ly)
    
    # 构建瀑布图
    fig_waterfall_macro = go.Figure(go.Waterfall(
        name="RevPAR 归因",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["去年同期 RevPAR", "入住率贡献 (Volume)", "房价贡献 (Rate)", "交叉效应 (Interaction)", "今年实际 RevPAR"],
        textposition="outside",
        text=[1410, f"+{vol_effect:.0f}", f"+{rate_effect:.0f}", f"+{mix_effect:.0f}", 1600],
        y=[1410, vol_effect, rate_effect, mix_effect, 1600],
        connector={"line":{"color":"rgb(63, 63, 63)"}},
        decreasing={"marker":{"color":"#e74c3c"}},
        increasing={"marker":{"color":"#2ecc71"}},
        totals={"marker":{"color":"#3498db"}}
    ))
    fig_waterfall_macro.update_layout(height=400, margin=dict(t=30, b=0))
    st.plotly_chart(fig_waterfall_macro, use_container_width=True)
    
    st.info("**💡 DRM 诊断结果**：本月 RevPAR 同比增长 HKD 190。通过模型拆解可见，**房价提升 (Rate Effect)** 贡献了绝大部分增量 (+HKD 98)，说明当前的提价策略是成功的，没有对客流量造成严重的吞噬。")

    st.markdown("---")

    st.markdown("### 2. 微观客源结构异动拆解 (Segment Contribution Attribution)")
    st.caption("深钻各个细分市场 (Segment) 对整体收益变化的具体贡献")
    
    col3_1, col3_2 = st.columns([1, 2])
    
    with col3_1:
        # 详细的数据透视表
        st.write("各客源类型贡献度明细")
        segment_data = pd.DataFrame({
            "客源类型": ["散客 (Retail)", "会员 (Bonvoy)", "团队 (Group)", "批发商 (Wholesale)"],
            "量价总贡献 (HKD)": [120, 85, -30, 15],
            "主要原因": ["ADR 提升主导", "量价齐升", "接团量大幅减少", "基础盘稳定"]
        })
        
        def format_color(val):
            if isinstance(val, (int, float)):
                return 'color: green' if val > 0 else 'color: red'
            return ''
            
        st.dataframe(segment_data.style.map(format_color, subset=['量价总贡献 (HKD)']), use_container_width=True)
        
    with col3_2:
        # 客源结构微观瀑布图
        fig_waterfall_micro = go.Figure(go.Waterfall(
            name="Segment 归因",
            orientation="h", # 横向瀑布图适合展示多个 Segment
            measure=["absolute", "relative", "relative", "relative", "relative", "total"],
            y=["去年收益基准", "散客贡献", "会员贡献", "团队客流失", "批发商微增", "今年总收益"],
            x=[800000, 120000, 85000, -30000, 15000, 990000],
            connector={"line":{"color":"rgb(63, 63, 63)"}},
            decreasing={"marker":{"color":"#e74c3c"}},
            increasing={"marker":{"color":"#2ecc71"}},
            totals={"marker":{"color":"#9b59b6"}}
        ))
        fig_waterfall_micro.update_layout(height=350, margin=dict(t=10, b=0, l=0, r=0))
        st.plotly_chart(fig_waterfall_micro, use_container_width=True)
        
    st.warning("🚨 **结构化预警 (Displacement Alert)**：虽然整体收益上涨，但团队业务 (Group) 贡献为负。如果这是主动用高价散客置换掉低价团队客的结果，则策略健康；如果是因为销售部门未达成目标，则需要联合 DOSM（销售总监）复盘团队 MICE 报价体系。")


with tab4:
    st.markdown("### 1. 渠道分销成本 (Distribution Costs & COA)")
    st.caption("剥离 OTA 佣金，看清酒店装进口袋的真实净收益 (Net RevPAR)")
    
    col4_1, col4_2 = st.columns([1.5, 1])
    with col4_1:
        # 模拟不同渠道的 Gross vs Net 收益
        channels_cost = ['Marriott 直销', '携程 (Ctrip)', 'Booking.com', '传统批发商 (B2B)', '公司协议价 (Corp)']
        gross_adr = [1850, 1900, 1880, 1500, 1600]
        commissions = [20, 285, 300, 150, 0] # 模拟佣金/渠道费用估算
        net_adr = [g - c for g, c in zip(gross_adr, commissions)]
        
        fig_net_adr = go.Figure()
        fig_net_adr.add_trace(go.Bar(x=channels_cost, y=net_adr, name='Net ADR (净房价)', marker_color='#27ae60'))
        fig_net_adr.add_trace(go.Bar(x=channels_cost, y=commissions, name='获客成本/佣金 (COA)', marker_color='#e74c3c'))
        
        fig_net_adr.update_layout(
            barmode='stack', 
            title="各渠道 ADR 与获客成本拆解 (HKD)",
            height=350, margin=dict(t=30, b=0)
        )
        st.plotly_chart(fig_net_adr, use_container_width=True)

    with col4_2:
        st.write("📈 **专家财务视角**")
        st.metric(label="当前整体毛收益 (Gross RevPAR)", value="HKD 1,600")
        st.metric(label="当前整体净收益 (Net RevPAR)", value="HKD 1,385", delta="-13.4% (整体渠道费率)", delta_color="inverse")
        st.info("💡 **DRM 策略点**：Booking.com 带来了高 ADR，但扣除 15%+ 的高额佣金后，其实际净收益（Net ADR=1580）反而低于万豪官网直销（Net ADR=1830）。本周末应立即对高佣金 OTA 实施 **渠道关闭或房型限制 (Channel Squeezing)**，逼迫流量回流直销。")

    st.markdown("---")

# ==========================================
# 6. 标签页 5: 全面收益管理 (TrevPAR & Ancillary)
# ==========================================
with tab5:
    st.markdown("### 1. 综合体总营收监控 (Integrated Resort TrevPAR)")
    st.caption("突破客房思维，监控餐饮 (F&B)、SPA 及新濠影汇水上乐园门票带来的衍生价值")
    
    c5_1, c5_2 = st.columns(2)
    
    with c5_1:
        # 饼图：总体收入结构
        revenue_streams = ['客房 (Rooms)', '餐饮 (F&B)', '宴会/会议 (MICE Space)', 'SPA/休闲', '水上乐园/娱乐门票']
        rev_values = [60, 20, 10, 5, 5]
        
        fig_trev = px.pie(
            values=rev_values, names=revenue_streams, hole=0.5,
            color_discrete_sequence=['#8e44ad', '#f39c12', '#2980b9', '#16a085', '#e74c3c']
        )
        fig_trev.update_traces(textposition='inside', textinfo='percent+label')
        fig_trev.update_layout(title="本月总收入构成 (Total Revenue Mix)", height=350, margin=dict(t=30, b=0))
        st.plotly_chart(fig_trev, use_container_width=True)
        
    with c5_2:
        st.markdown("#### 🔥 餐饮客房联合置换分析 (Displacement Analysis)")
        st.write("案例：本周五接到一个需要 **50间房 + 1个大宴会厅** 的医药公司团队 (MICE) 询价，但他们给的客房预算极低。")
        
        disp_df = pd.DataFrame({
            "评估维度": ["预测散客房价 (ADR)", "团队目标房价", "客房直接损失 (Displacement)", "团队附带餐饮/会议消费", "总体利润差额"],
            "数值": ["HKD 2,000", "HKD 1,300", "- HKD 35,000", "+ HKD 80,000", "**+ HKD 45,000**"]
        })
        st.table(disp_df)
        st.success("**🎯 专家决策通过**：虽然接这个低价团队会拉低当天的客房 ADR，但由于其高额的宴会餐饮（F&B）消费，整体（TrevPAR）对酒店是有利可图的。应联合餐饮总监（DOFB）和销售总监一起接下此单。")