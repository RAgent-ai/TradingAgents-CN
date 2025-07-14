"""
历史记录页面
"""

import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
import sys

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from web.utils.report_storage import (
    get_all_stocks, 
    get_stock_reports, 
    load_report,
    delete_report
)
from web.components.results_display import render_results

def render_history_page():
    """渲染历史记录页面"""
    st.header("📈 历史分析记录")
    
    # 获取所有有报告的股票
    stocks = get_all_stocks()
    
    if not stocks:
        st.info("暂无历史分析记录")
        return
    
    # 创建两列布局
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("股票列表")
        
        # 显示股票列表
        selected_stock = st.selectbox(
            "选择股票",
            options=[s['symbol'] for s in stocks],
            format_func=lambda x: f"{x} ({next(s['report_count'] for s in stocks if s['symbol'] == x)} 份报告)"
        )
        
        # 显示统计信息
        if selected_stock:
            stock_info = next(s for s in stocks if s['symbol'] == selected_stock)
            st.metric("报告数量", f"{stock_info['report_count']} 份")
    
    with col2:
        if selected_stock:
            st.subheader(f"{selected_stock} 的历史报告")
            
            # 获取该股票的所有报告
            reports = get_stock_reports(selected_stock)
            
            if reports:
                # 创建报告选择器
                report_options = []
                for report in reports:
                    metadata = report['metadata']
                    generated_at = datetime.fromisoformat(metadata['generated_at'])
                    display_text = (
                        f"{generated_at.strftime('%Y-%m-%d %H:%M')} | "
                        f"分析日期: {metadata['analysis_date']} | "
                        f"建议: {report['summary']['action']} | "
                        f"置信度: {report['summary']['confidence']}"
                    )
                    report_options.append((display_text, report))
                
                selected_report_text = st.selectbox(
                    "选择报告",
                    options=[opt[0] for opt in report_options]
                )
                
                # 找到选中的报告
                selected_report = next(opt[1] for opt in report_options if opt[0] == selected_report_text)
                
                # 操作按钮
                col1, col2, col3 = st.columns([1, 1, 4])
                
                with col1:
                    if st.button("📄 查看报告", type="primary"):
                        # 加载完整报告
                        full_report = load_report(selected_report['filepath'])
                        st.session_state.viewing_report = full_report['results']
                
                with col2:
                    if st.button("🗑️ 删除报告"):
                        if st.checkbox("确认删除？"):
                            delete_report(selected_report['filepath'])
                            st.success("报告已删除")
                            st.rerun()
                
                # 显示报告摘要
                st.markdown("---")
                st.subheader("报告摘要")
                
                summary = selected_report['summary']
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("投资建议", summary['action'])
                
                with col2:
                    confidence = summary['confidence']
                    if isinstance(confidence, (int, float)):
                        st.metric("置信度", f"{confidence:.1%}")
                    else:
                        st.metric("置信度", str(confidence))
                
                with col3:
                    target_price = summary['target_price']
                    if target_price and isinstance(target_price, (int, float)):
                        # 判断是否为A股
                        is_china = selected_stock.isdigit() and len(selected_stock) == 6
                        currency = "¥" if is_china else "$"
                        st.metric("目标价位", f"{currency}{target_price:.2f}")
                    else:
                        st.metric("目标价位", "待分析")
                
                # 如果选择了查看报告，显示完整报告
                if 'viewing_report' in st.session_state:
                    st.markdown("---")
                    st.subheader("完整报告")
                    render_results(st.session_state.viewing_report)
                    
                    # 清除查看状态
                    if st.button("关闭报告"):
                        del st.session_state.viewing_report
                        st.rerun()
            else:
                st.info(f"暂无 {selected_stock} 的历史报告")

def main():
    """主函数"""
    render_history_page()

if __name__ == "__main__":
    main()