"""
报告存储和管理功能
"""

import os
import json
import datetime
from pathlib import Path

def get_reports_dir():
    """获取报告存储目录"""
    # 在项目根目录下创建 analysis_reports 目录
    project_root = Path(__file__).parent.parent.parent
    reports_dir = project_root / "analysis_reports"
    reports_dir.mkdir(exist_ok=True)
    return reports_dir

def save_analysis_report(stock_symbol, analysis_date, results):
    """
    保存分析报告到文件
    
    Args:
        stock_symbol: 股票代码
        analysis_date: 分析日期
        results: 分析结果字典
    """
    # 创建股票目录
    reports_dir = get_reports_dir()
    stock_dir = reports_dir / stock_symbol.upper()
    stock_dir.mkdir(exist_ok=True)
    
    # 生成文件名: YYYYMMDD_HHMMSS_report.json
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_report.json"
    filepath = stock_dir / filename
    
    # 添加元数据
    report_data = {
        "metadata": {
            "stock_symbol": stock_symbol.upper(),
            "analysis_date": str(analysis_date),
            "generated_at": datetime.datetime.now().isoformat(),
            "filename": filename
        },
        "results": results
    }
    
    # 保存为JSON文件
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    # 同时生成纯文本版本
    save_text_report(stock_dir, timestamp, stock_symbol, results)
    
    print(f"📁 报告已保存到: {filepath}")
    return str(filepath)

def save_text_report(stock_dir, timestamp, stock_symbol, results):
    """
    保存纯文本版本的报告
    """
    filename = f"{timestamp}_report.txt"
    filepath = stock_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        # 写入标题
        f.write(f"{'='*60}\n")
        f.write(f"股票分析报告 - {stock_symbol}\n")
        f.write(f"生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*60}\n\n")
        
        # 写入决策摘要
        if 'decision' in results:
            decision = results['decision']
            f.write("📊 投资决策摘要\n")
            f.write("-" * 40 + "\n")
            f.write(f"投资建议: {decision.get('action', 'N/A')}\n")
            f.write(f"置信度: {decision.get('confidence', 'N/A')}\n")
            f.write(f"风险评分: {decision.get('risk_score', 'N/A')}\n")
            f.write(f"目标价位: {decision.get('target_price', 'N/A')}\n")
            if 'reasoning' in decision:
                f.write(f"\n分析推理:\n{decision['reasoning']}\n")
            f.write("\n")
        
        # 写入详细分析
        if 'state' in results:
            state = results['state']
            
            # 市场分析
            if 'market_report' in state:
                f.write("📈 市场技术分析\n")
                f.write("-" * 40 + "\n")
                f.write(state['market_report'])
                f.write("\n\n")
            
            # 基本面分析
            if 'fundamentals_report' in state:
                f.write("💰 基本面分析\n")
                f.write("-" * 40 + "\n")
                f.write(state['fundamentals_report'])
                f.write("\n\n")
            
            # 情绪分析
            if 'sentiment_report' in state:
                f.write("💭 市场情绪分析\n")
                f.write("-" * 40 + "\n")
                f.write(state['sentiment_report'])
                f.write("\n\n")
            
            # 新闻分析
            if 'news_report' in state:
                f.write("📰 新闻事件分析\n")
                f.write("-" * 40 + "\n")
                f.write(state['news_report'])
                f.write("\n\n")
            
            # 风险评估
            if 'risk_assessment' in state:
                f.write("⚠️ 风险评估\n")
                f.write("-" * 40 + "\n")
                f.write(state['risk_assessment'])
                f.write("\n\n")
            
            # 投资建议
            if 'investment_plan' in state:
                f.write("📋 投资建议\n")
                f.write("-" * 40 + "\n")
                f.write(state['investment_plan'])
                f.write("\n\n")
        
        # 写入配置信息
        f.write("⚙️ 分析配置\n")
        f.write("-" * 40 + "\n")
        f.write(f"LLM提供商: {results.get('llm_provider', 'N/A')}\n")
        f.write(f"模型: {results.get('llm_model', 'N/A')}\n")
        f.write(f"分析师: {', '.join(results.get('analysts', []))}\n")
        f.write("\n")
        
        # 写入免责声明
        f.write("⚠️ 重要免责声明\n")
        f.write("-" * 40 + "\n")
        f.write("本报告仅供参考，不构成投资建议。\n")
        f.write("投资有风险，决策需谨慎。\n")

def get_stock_reports(stock_symbol):
    """
    获取某个股票的所有历史报告
    
    Args:
        stock_symbol: 股票代码
        
    Returns:
        报告列表，按时间倒序排列
    """
    reports_dir = get_reports_dir()
    stock_dir = reports_dir / stock_symbol.upper()
    
    if not stock_dir.exists():
        return []
    
    reports = []
    for json_file in stock_dir.glob("*_report.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                reports.append({
                    'filename': json_file.name,
                    'filepath': str(json_file),
                    'metadata': data['metadata'],
                    'summary': {
                        'action': data['results'].get('decision', {}).get('action', 'N/A'),
                        'confidence': data['results'].get('decision', {}).get('confidence', 'N/A'),
                        'target_price': data['results'].get('decision', {}).get('target_price', 'N/A')
                    }
                })
        except Exception as e:
            print(f"读取报告失败 {json_file}: {e}")
    
    # 按生成时间倒序排列
    reports.sort(key=lambda x: x['metadata']['generated_at'], reverse=True)
    return reports

def get_all_stocks():
    """获取所有有历史报告的股票列表"""
    reports_dir = get_reports_dir()
    stocks = []
    
    for stock_dir in reports_dir.iterdir():
        if stock_dir.is_dir():
            # 统计报告数量
            report_count = len(list(stock_dir.glob("*_report.json")))
            if report_count > 0:
                stocks.append({
                    'symbol': stock_dir.name,
                    'report_count': report_count
                })
    
    # 按报告数量倒序排列
    stocks.sort(key=lambda x: x['report_count'], reverse=True)
    return stocks

def load_report(filepath):
    """加载完整的报告内容"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def delete_report(filepath):
    """删除报告文件"""
    json_path = Path(filepath)
    txt_path = json_path.with_suffix('.txt')
    
    # 删除JSON文件
    if json_path.exists():
        json_path.unlink()
    
    # 删除对应的文本文件
    if txt_path.exists():
        txt_path.unlink()