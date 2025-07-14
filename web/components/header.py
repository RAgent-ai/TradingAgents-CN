"""
页面头部组件
"""

import streamlit as st

def render_header():
    """渲染页面头部"""
    
    # 仅显示简洁的标题
    st.title("🚀 TradingAgents-CN 股票分析平台")
    st.markdown("---")
