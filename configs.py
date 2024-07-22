local_llm_config={
    "config_list": [
        {
            "model": "NotRequired", # Loaded with LiteLLM command
            "api_key": "NotRequired", # Not needed
            "base_url": "http://localhost:4000"  # Your LiteLLM URL
        }
    ],
    "cache_seed": None # Turns off caching, useful for testing different models
}

llama_groq_config = {
    "config_list": [
        {
            "model": "llama3-groq-tool-use",
            "base_url": "http://localhost:11434/v1",
            "api_key": "ollama",
        }
    ]
}

codellama_config = {
    "config_list": [
        {
            "model": "codellama",
            "base_url": "http://localhost:11434/v1",
            "api_key": "codellama",
        }
    ]
}

llama_instruct_config = {
    "config_list": [
        {
            "model": "llama3:8b-instruct-q6_K",
            "base_url": "http://localhost:11434/v1",
            "api_key": "llama3:8b-instruct-q6_K",
        }
    ]
}
