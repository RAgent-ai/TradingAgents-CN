# CLAUDE.md

这个文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

这是 TradingAgents 的中文增强版，基于 TauricResearch 的原始项目开发，专为中文用户提供完整的文档体系和本地化支持。

### 核心增强功能

| 功能 | 说明 |
|------|------|
| 📚 中文文档 | docs/ 目录中 50,000+ 字的完整中文文档 |
| 🌐 Web 界面 | 基于 Streamlit 的现代化 Web 应用 |
| 🇨🇳 A 股支持 | 通过 pytdx 完全支持 A 股实时数据 |
| 🧠 国产 LLM | 支持阿里百炼/通义千问模型 |
| 🗄️ 数据库 | MongoDB + Redis 数据持久化和缓存 |
| ⚙️ 统一配置 | 基于 .env 的集中配置管理 |

## 常用开发命令

### 安装
```bash
# 创建虚拟环境
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows

# 安装基础依赖
pip install -r requirements.txt

# 安装数据库支持（可选）
pip install -r requirements_db.txt  # MongoDB + Redis

# 安装 A 股数据支持（推荐）
pip install pytdx
```

### 运行应用

```bash
# 运行 Web 界面（推荐）
streamlit run web/app.py

# 运行 CLI
python -m cli.main

# 查看数据配置
python -m cli.main data-config --show

# 启动数据库服务（如果使用）
docker-compose up -d
```

### 测试
```bash
# 运行所有测试
python -m pytest tests/

# 运行特定测试
python tests/test_analysis.py

# 集成测试
python tests/integration/test_dashscope_integration.py

# A 股数据测试
python tests/test_tdx_integration.py
```

## 系统架构

### 多智能体架构
基于 LangGraph 构建的多智能体系统：

1. **智能体团队**：
   - **分析师团队**：基本面、市场、新闻、社交媒体分析师
   - **研究员团队**：看涨和看跌研究员进行辩论
   - **交易员**：基于综合分析做出交易决策
   - **风险管理团队**：保守、中立、激进风险评估
   - **管理层**：研究经理和风险经理协调决策

2. **数据流程**：
   ```
   输入（股票代码、日期）
      ↓
   数据获取（多源数据）
      ↓
   并行分析师分析
      ↓
   研究员辩论
      ↓
   交易决策
      ↓
   风险评估
      ↓
   最终输出
   ```

3. **LangGraph 工作流**（`graph/trading_graph.py`）：
   - 状态机模式管理智能体协作
   - 条件路由基于分析结果
   - 可配置的辩论轮数和递归限制

### 中文版特色功能

1. **Web 界面**（`web/`）：
   - Streamlit 构建的响应式界面
   - 实时进度跟踪和可视化
   - 5 级研究深度配置（2-25分钟）
   - Token 使用统计和成本追踪

2. **数据源集成**：
   - **A 股数据**：通达信 API (`tdx_utils.py`)
   - **美股数据**：FinnHub、Yahoo Finance
   - **新闻数据**：Google News、财经新闻
   - **社交媒体**：Reddit 情绪分析

3. **LLM 支持**：
   - **Google AI**：Gemini 系列模型（默认）
   - **阿里百炼**：通义千问系列
   - **OpenAI**：GPT 系列
   - **Anthropic**：Claude 系列

4. **数据存储**：
   - **MongoDB**：历史数据持久化
   - **Redis**：高速缓存
   - **智能降级**：MongoDB → API → 文件缓存

## 环境配置

### 必需的环境变量
```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，配置必需项：
GOOGLE_API_KEY=your_google_api_key      # Google AI API密钥（必需）
FINNHUB_API_KEY=your_finnhub_api_key    # 金融数据API密钥（必需）

# LLM 配置（可选，有默认值）
LLM_PROVIDER=google                      # LLM提供商
DEEP_THINK_MODEL=gemini-2.0-flash       # 深度分析模型
QUICK_THINK_MODEL=gemini-1.5-flash      # 快速分析模型

# 数据库配置（可选）
MONGODB_ENABLED=false                    # 启用 MongoDB
REDIS_ENABLED=false                      # 启用 Redis
```

### API 密钥获取
1. **Google AI**: https://ai.google.dev/ （免费，推荐）
2. **FinnHub**: https://finnhub.io/ （免费版足够）
3. **阿里百炼**: https://dashscope.aliyun.com/ （备选）

### 模型配置说明
- 系统默认使用 Google Gemini 模型
- 模型选择通过环境变量控制，不在前端暴露
- 支持动态切换不同 LLM 提供商

## 关键实现细节

1. **状态管理**：使用 TypedDict 定义智能体状态
2. **内存系统**：ChromaDB 向量数据库存储历史记忆
3. **缓存策略**：多层缓存减少 API 调用成本
4. **错误处理**：优雅降级和自动重试机制
5. **并行处理**：分析师并行工作提高效率

## 重要注意事项

1. **API 密钥安全**：
   - 永远不要将 `.env` 文件提交到 Git
   - 使用 `.env.example` 作为模板
   - 敏感信息仅保存在本地

2. **中文版特性**：
   - 数据库使用非标准端口避免冲突
   - A 股代码格式：6位数字（如 000001、600519）
   - 支持中文公司名称查询

3. **性能优化**：
   - 启用数据库可显著提升性能
   - 使用缓存减少重复 API 调用
   - 合理设置研究深度平衡时间和质量

4. **开发建议**：
   - 优先使用 Web 界面进行测试
   - 查看 `examples/` 目录了解用法
   - 参考 `docs/` 完整文档深入了解

## 项目结构

```
TradingAgents-CN/
├── web/                    # Web 界面
│   ├── app.py             # 主应用入口
│   ├── components/        # UI 组件
│   └── pages/            # 功能页面
├── tradingagents/         # 核心业务逻辑
│   ├── agents/           # 智能体实现
│   ├── graph/            # LangGraph 工作流
│   ├── dataflows/        # 数据处理
│   └── llm_adapters/     # LLM 适配器
├── docs/                  # 中文文档（50,000+字）
├── examples/             # 使用示例
├── tests/                # 测试用例
└── scripts/              # 工具脚本
```

# 重要指导原则
- 优先编辑现有文件而非创建新文件
- 仅在必要时创建新文件
- 不要主动创建文档文件，除非用户明确要求
- 遵循项目现有的代码风格和命名规范