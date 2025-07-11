# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Setup
```bash
# Create virtual environment
python -m venv venv
# Activate virtual environment (Windows)
.\venv\Scripts\activate
# Activate virtual environment (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# Install database dependencies (optional)
pip install -r requirements_db.txt

# Setup environment
cp .env.example .env
# Edit .env to add API keys (at minimum: DASHSCOPE_API_KEY and FINNHUB_API_KEY)
```

### Running the Application
```bash
# Web interface (recommended)
streamlit run web/app.py

# Command line interface
python -m cli.main

# Direct Python usage
python examples/dashscope/demo_dashscope_chinese.py
```

### Testing
```bash
# Run integration tests
python tests/integration/test_dashscope_integration.py

# Test specific functionality
python tests/test_tdx_integration.py  # A股数据测试
python tests/test_config_management.py  # 配置管理测试
```

### Database Management (Optional)
```bash
# Start MongoDB and Redis with Docker
docker-compose up -d

# Initialize database
python scripts/setup/init_database.py

# Check database status
python scripts/setup/check_system_status.py
```

## High-Level Architecture

TradingAgents-CN is a multi-agent AI framework for financial trading decisions, built on LangGraph. It simulates a real trading firm's decision-making process.

### Core Components

1. **Multi-Agent System** (`tradingagents/agents/`)
   - **Analysts**: FundamentalsAnalyst, MarketAnalyst, NewsAnalyst, SocialMediaAnalyst
   - **Researchers**: BullResearcher, BearResearcher (debate mechanism)
   - **Trader**: Makes final trading decisions
   - **Risk Management**: Aggressive, Conservative, Neutral debators
   - **Managers**: ResearchManager, RiskManager coordinate teams

2. **Graph Orchestration** (`tradingagents/graph/`)
   - `TradingAgentsGraph`: Main orchestrator using LangGraph
   - `ConditionalLogic`: Routes between agent states
   - `Propagator`: Manages agent communication
   - `SignalProcessor`: Processes trading signals

3. **Data Layer** (`tradingagents/dataflows/`)
   - **US Stocks**: FinnHub, Yahoo Finance integration
   - **A股 (China)**: TDX (通达信) API integration via pytdx
   - **News**: Google News, real-time news APIs
   - **Social**: Reddit sentiment analysis
   - **Caching**: Multi-level cache (Redis → MongoDB → API)

4. **LLM Adapters** (`tradingagents/llm_adapters/`)
   - DashScope (阿里百炼): Primary for Chinese users
   - Google AI: Gemini models support
   - OpenAI/Anthropic: Available with configuration

5. **Web Interface** (`web/`)
   - Streamlit-based UI with 5 research depth levels
   - Configuration management
   - Token usage tracking
   - Cache management

### Key Design Patterns

- **Agent State Management**: Each agent maintains its state through LangGraph nodes
- **Debate Mechanism**: Bull vs Bear researchers debate before final decision
- **Risk Assessment**: Triple-perspective risk evaluation
- **Fallback System**: MongoDB → TDX API → Local cache for reliability
- **Async Processing**: Parallel agent analysis for performance

### Important Configurations

- **Research Depth Levels**: 1 (fast, 2-4min) to 5 (comprehensive, 15-25min)
- **LLM Selection**: Configure via `llm_provider`, `deep_think_llm`, `quick_think_llm`
- **Data Sources**: Enable/disable via environment variables (MONGODB_ENABLED, REDIS_ENABLED)
- **API Keys**: Required minimum - DASHSCOPE_API_KEY, FINNHUB_API_KEY

### Code Flow Example

1. User requests analysis for stock (e.g., "AAPL" or "600519")
2. TradingAgentsGraph initializes with configuration
3. Analysts gather data in parallel (market, fundamentals, news, social)
4. Research Manager coordinates analyst outputs
5. Bull and Bear researchers debate investment thesis
6. Risk Management team evaluates from three perspectives
7. Trader makes final decision with confidence and risk scores
8. Results returned with structured recommendation

This architecture enables sophisticated financial analysis while remaining modular and extensible.