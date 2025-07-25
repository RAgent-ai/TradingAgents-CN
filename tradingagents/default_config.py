import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": os.path.join(os.path.expanduser("~"), "Documents", "TradingAgents", "data"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings - 从环境变量读取，默认使用 Google Gemini
    "llm_provider": os.getenv("LLM_PROVIDER", "google"),
    "deep_think_llm": os.getenv("DEEP_THINK_MODEL", "gemini-2.0-flash"),
    "quick_think_llm": os.getenv("QUICK_THINK_MODEL", "gemini-1.5-flash"),
    "backend_url": os.getenv("LLM_BACKEND_URL", "https://api.openai.com/v1"),
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Tool settings
    "online_tools": True,

    # Note: Database and cache configuration is now managed by .env file and config.database_manager
    # No database/cache settings in default config to avoid configuration conflicts
}
