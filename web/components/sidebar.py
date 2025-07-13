"""
侧边栏组件
"""

import streamlit as st
import os

def render_sidebar():
    """渲染侧边栏配置"""
    
    with st.sidebar:
        st.header("🔧 系统配置")
        
        # API密钥状态
        st.subheader("🔑 API密钥状态")
        
        # 检查各个API密钥
        google_key = os.getenv("GOOGLE_API_KEY")
        finnhub_key = os.getenv("FINNHUB_API_KEY")
        dashscope_key = os.getenv("DASHSCOPE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        # Google AI (主要)
        if google_key:
            st.success(f"✅ Google AI: {google_key[:12]}...")
        else:
            st.error("❌ Google AI: 未配置")
        
        # 金融数据
        if finnhub_key:
            st.success(f"✅ 金融数据: {finnhub_key[:12]}...")
        else:
            st.error("❌ 金融数据: 未配置")
        
        # 其他可选API
        if dashscope_key:
            st.info(f"ℹ️ 阿里百炼: {dashscope_key[:12]}... (备用)")
        
        if openai_key:
            st.info(f"ℹ️ OpenAI: {openai_key[:12]}... (备用)")
        
        st.markdown("---")
        
        # AI模型信息 (只显示，不允许选择)
        st.subheader("🧠 AI模型配置")
        
        # 从环境变量读取配置
        llm_provider = os.getenv("LLM_PROVIDER", "google")
        deep_think_model = os.getenv("DEEP_THINK_MODEL", "gemini-2.0-flash")
        quick_think_model = os.getenv("QUICK_THINK_MODEL", "gemini-1.5-flash")
        
        # 显示当前配置
        st.info(f"""
        **当前配置:**
        - 提供商: {llm_provider.upper()}
        - 深度分析模型: {deep_think_model}
        - 快速分析模型: {quick_think_model}
        
        💡 模型配置通过环境变量设置，请在 .env 文件中修改
        """)
        
        # 高级设置
        with st.expander("⚙️ 高级设置"):
            enable_memory = st.checkbox(
                "启用记忆功能",
                value=False,
                help="启用智能体记忆功能（可能影响性能）"
            )
            
            enable_debug = st.checkbox(
                "调试模式",
                value=False,
                help="启用详细的调试信息输出"
            )
            
            max_tokens = st.slider(
                "最大输出长度",
                min_value=1000,
                max_value=8000,
                value=4000,
                step=500,
                help="AI模型的最大输出token数量"
            )
        
        st.markdown("---")
        
        # 系统信息
        st.subheader("ℹ️ 系统信息")
        
        st.info(f"""
        **版本**: 1.0.0
        **框架**: Streamlit + LangGraph
        **AI模型**: {llm_provider.upper()} ({deep_think_model})
        **数据源**: FinnHub API
        """)
        
        # 帮助链接
        st.subheader("📚 帮助资源")
        
        st.markdown("""
        - [📖 使用文档](https://github.com/TauricResearch/TradingAgents)
        - [🐛 问题反馈](https://github.com/TauricResearch/TradingAgents/issues)
        - [💬 讨论社区](https://github.com/TauricResearch/TradingAgents/discussions)
        - [🔧 API密钥配置](../docs/security/api_keys_security.md)
        """)
    
    # 返回配置（从环境变量读取）
    return {
        'llm_provider': llm_provider,
        'llm_model': deep_think_model,  # 使用深度分析模型作为主模型
        'enable_memory': enable_memory,
        'enable_debug': enable_debug,
        'max_tokens': max_tokens
    }
