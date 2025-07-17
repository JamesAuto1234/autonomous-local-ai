from pathlib import Path
import os
from typing import Optional, Dict, Any, Union
from functools import lru_cache

DEFAULT_MODEL_DIR = Path.cwd() / "models"


class BaseConfig:
    """Base configuration class with common utilities."""
    
    @staticmethod
    def get_env_int(key: str, default: int, min_val: int = 0, max_val: Optional[int] = None) -> int:
        """Get environment variable as integer with validation."""
        value = int(os.getenv(key, str(default)))
        if value < min_val:
            raise ValueError(f"{key} must be >= {min_val}, got {value}")
        if max_val is not None and value > max_val:
            raise ValueError(f"{key} must be <= {max_val}, got {value}")
        return value
    
    @staticmethod
    def get_env_float(key: str, default: float, min_val: float = 0.0, max_val: Optional[float] = None) -> float:
        """Get environment variable as float with validation."""
        value = float(os.getenv(key, str(default)))
        if value < min_val:
            raise ValueError(f"{key} must be >= {min_val}, got {value}")
        if max_val is not None and value > max_val:
            raise ValueError(f"{key} must be <= {max_val}, got {value}")
        return value


class PerformanceConfig(BaseConfig):
    """Performance and timeout configuration settings."""
    
    # Dynamic unload feature settings
    IDLE_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_IDLE_TIMEOUT", 1800, 60)  # 30 min, min 1 min
    UNLOAD_CHECK_INTERVAL: int = BaseConfig.get_env_int("LOCAL_AI_UNLOAD_CHECK_INTERVAL", 30, 5)  # 30 sec, min 5 sec
    UNLOAD_LOG_INTERVAL: int = BaseConfig.get_env_int("LOCAL_AI_UNLOAD_LOG_INTERVAL", 300, 60)  # 5 min, min 1 min
    UNLOAD_MAX_CONSECUTIVE_ERRORS: int = BaseConfig.get_env_int("LOCAL_AI_UNLOAD_MAX_CONSECUTIVE_ERRORS", 5, 1, 20)
    UNLOAD_ERROR_SLEEP_MULTIPLIER: int = BaseConfig.get_env_int("LOCAL_AI_UNLOAD_ERROR_SLEEP_MULTIPLIER", 2, 1, 10)
    
    # Stream settings - consolidated and optimized
    STREAM_CLEANUP_INTERVAL: int = BaseConfig.get_env_int("LOCAL_AI_STREAM_CLEANUP_INTERVAL", 60, 10)  # 1 min, min 10 sec
    STREAM_CLEANUP_ERROR_SLEEP: int = BaseConfig.get_env_int("LOCAL_AI_STREAM_CLEANUP_ERROR_SLEEP", 60, 10)  # 1 min, min 10 sec
    STREAM_STALE_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_STREAM_STALE_TIMEOUT", 600, 60)  # 10 min, min 1 min
    STREAM_TIMEOUT: float = BaseConfig.get_env_float("LOCAL_AI_STREAM_TIMEOUT", 7200.0, 30.0)  # 2 hours, min 30 sec
    STREAM_CHUNK_SIZE: int = BaseConfig.get_env_int("LOCAL_AI_STREAM_CHUNK_SIZE", 16384, 1024, 1048576)  # 16KB, 1KB-1MB
    
    # Model operations
    MODEL_SWITCH_VERIFICATION_DELAY: float = BaseConfig.get_env_float("LOCAL_AI_MODEL_SWITCH_VERIFICATION_DELAY", 0.5, 0.1, 5.0)
    MODEL_SWITCH_MAX_RETRIES: int = BaseConfig.get_env_int("LOCAL_AI_MODEL_SWITCH_MAX_RETRIES", 3, 1, 10)
    MODEL_SWITCH_STREAM_TIMEOUT: float = BaseConfig.get_env_float("LOCAL_AI_MODEL_SWITCH_STREAM_TIMEOUT", 30.0, 5.0)
    
    # Queue and processing - optimized defaults
    QUEUE_BACKPRESSURE_TIMEOUT: float = BaseConfig.get_env_float("LOCAL_AI_QUEUE_BACKPRESSURE_TIMEOUT", 30.0, 1.0)
    PROCESS_CHECK_INTERVAL: float = BaseConfig.get_env_float("LOCAL_AI_PROCESS_CHECK_INTERVAL", 0.1, 0.01, 1.0)
    MAX_QUEUE_SIZE: int = BaseConfig.get_env_int("LOCAL_AI_MAX_QUEUE_SIZE", 100, 10, 1000)  # Increased from 50
    HEALTH_CHECK_INTERVAL: int = BaseConfig.get_env_int("LOCAL_AI_HEALTH_CHECK_INTERVAL", 2, 1, 60)
    
    # Timeouts - consolidated and optimized
    SERVICE_START_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_SERVICE_START_TIMEOUT", 3600, 60)  # 1 hour, min 1 min
    HTTP_TIMEOUT: float = BaseConfig.get_env_float("LOCAL_AI_HTTP_TIMEOUT", 1800.0, 30.0)  # 30 min, more reasonable
    
    # Shutdown timeouts
    SHUTDOWN_TASK_TIMEOUT: float = BaseConfig.get_env_float("LOCAL_AI_SHUTDOWN_TASK_TIMEOUT", 10.0, 1.0, 60.0)
    SHUTDOWN_SERVER_TIMEOUT: float = BaseConfig.get_env_float("LOCAL_AI_SHUTDOWN_SERVER_TIMEOUT", 15.0, 1.0, 60.0)
    SHUTDOWN_CLIENT_TIMEOUT: float = BaseConfig.get_env_float("LOCAL_AI_SHUTDOWN_CLIENT_TIMEOUT", 5.0, 1.0, 30.0)
    
    # HTTP connection pooling - optimized
    POOL_CONNECTIONS: int = BaseConfig.get_env_int("LOCAL_AI_POOL_CONNECTIONS", 100, 10, 500)  # Increased from 50
    POOL_KEEPALIVE: int = BaseConfig.get_env_int("LOCAL_AI_POOL_KEEPALIVE", 20, 5, 100)  # Increased from 10
    
    # Retry settings
    MAX_RETRIES: int = BaseConfig.get_env_int("LOCAL_AI_MAX_RETRIES", 3, 1, 10)  # Increased from 2
    RETRY_DELAY: float = BaseConfig.get_env_float("LOCAL_AI_RETRY_DELAY", 0.5, 0.1, 10.0)


class CoreConfig(BaseConfig):
    """Core service configuration settings."""
    
    # Lock and process management
    LOCK_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_LOCK_TIMEOUT", 1800, 60)  # 30 min, min 1 min
    PORT_CHECK_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_PORT_CHECK_TIMEOUT", 5, 1, 30)  # Increased from 2
    HEALTH_CHECK_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_HEALTH_CHECK_TIMEOUT", 300, 10)  # 5 min, min 10 sec
    PROCESS_TERM_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_PROCESS_TERM_TIMEOUT", 15, 5, 60)
    MAX_PORT_RETRIES: int = BaseConfig.get_env_int("LOCAL_AI_MAX_PORT_RETRIES", 10, 3, 50)  # Increased from 5
    
    # HTTP request settings
    REQUEST_RETRIES: int = BaseConfig.get_env_int("LOCAL_AI_REQUEST_RETRIES", 3, 1, 10)  # Increased from 2
    REQUEST_DELAY: int = BaseConfig.get_env_int("LOCAL_AI_REQUEST_DELAY", 2, 1, 10)
    REQUEST_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_REQUEST_TIMEOUT", 30, 5, 300)  # Increased from 8


class ModelConfig(BaseConfig):
    """Model-related configuration settings."""
    
    # Default model names
    DEFAULT_CHAT_MODEL: str = os.getenv("LOCAL_AI_DEFAULT_CHAT_MODEL", "llama-3.2-3b-instruct")
    DEFAULT_EMBED_MODEL: str = os.getenv("LOCAL_AI_DEFAULT_EMBED_MODEL", "text-embedding-3-small")
    DEFAULT_IMAGE_MODEL: str = os.getenv("LOCAL_AI_DEFAULT_IMAGE_MODEL", "stable-diffusion-v1-5")
    
    # Model limits - optimized
    MAX_MESSAGES: int = BaseConfig.get_env_int("LOCAL_AI_MAX_MESSAGES", 100, 10, 1000)  # Increased from 50
    DEFAULT_MAX_TOKENS: int = BaseConfig.get_env_int("LOCAL_AI_DEFAULT_MAX_TOKENS", 4096, 256, 32768)  # Decreased from 8192
    DEFAULT_CONTEXT_LENGTH: int = BaseConfig.get_env_int("LOCAL_AI_DEFAULT_CONTEXT_LENGTH", 16384, 1024, 131072)  # Decreased from 32768


class FilePathConfig(BaseConfig):
    """File path and directory configuration."""
    
    # Service files
    RUNNING_SERVICE_FILE: str = os.getenv("LOCAL_AI_RUNNING_SERVICE_FILE", "running_service.msgpack")
    START_LOCK_FILE: str = os.getenv("LOCAL_AI_START_LOCK_FILE", "start_lock.lock")
    
    # Directories
    LOGS_DIR: str = os.getenv("LOCAL_AI_LOGS_DIR", "logs")
    
    # External commands
    LLAMA_SERVER: Optional[str] = os.getenv("LOCAL_AI_LLAMA_SERVER")
    TAR_COMMAND: Optional[str] = os.getenv("LOCAL_AI_TAR_COMMAND", "tar")
    PIGZ_COMMAND: Optional[str] = os.getenv("LOCAL_AI_PIGZ_COMMAND", "pigz")
    CAT_COMMAND: Optional[str] = os.getenv("LOCAL_AI_CAT_COMMAND", "cat")


class NetworkConfig(BaseConfig):
    """Network and server configuration."""
    
    # Server settings
    DEFAULT_PORT: int = BaseConfig.get_env_int("LOCAL_AI_DEFAULT_PORT", 8080, 1024, 65535)
    DEFAULT_HOST: str = os.getenv("LOCAL_AI_DEFAULT_HOST", "0.0.0.0")
    
    # Download settings - optimized
    DEFAULT_CHUNK_SIZE: int = BaseConfig.get_env_int("LOCAL_AI_DEFAULT_CHUNK_SIZE", 65536, 1024, 1048576)  # 64KB, increased from 8KB
    MAX_CONCURRENT_DOWNLOADS: int = BaseConfig.get_env_int("LOCAL_AI_MAX_CONCURRENT_DOWNLOADS", 12, 1, 50)  # Increased from 8
    DOWNLOAD_TIMEOUT: int = BaseConfig.get_env_int("LOCAL_AI_DOWNLOAD_TIMEOUT", 600, 60, 3600)  # 10 min, increased from 5 min


class Config:
    """Main configuration class that aggregates all config sections."""
    
    def __init__(self):
        self.performance = PerformanceConfig()
        self.core = CoreConfig()
        self.model = ModelConfig()
        self.file_paths = FilePathConfig()
        self.network = NetworkConfig()
    
    @lru_cache(maxsize=1)
    def get_env_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get a cached summary of all configuration values for debugging."""
        config_sections = {
            "performance": self.performance,
            "core": self.core,
            "model": self.model,
            "file_paths": self.file_paths,
            "network": self.network
        }
        
        summary = {}
        for section_name, section_obj in config_sections.items():
            summary[section_name] = {
                attr: getattr(section_obj, attr)
                for attr in dir(section_obj)
                if not attr.startswith("_") and attr.isupper()
            }
        
        return summary
    
    def print_config(self) -> None:
        """Print current configuration for debugging."""
        import json
        print("Current Local AI Configuration:")
        print(json.dumps(self.get_env_summary(), indent=2, default=str))
    
    def validate_config(self) -> bool:
        """Validate configuration values for consistency."""
        try:
            # Validate timeout relationships
            if self.performance.SHUTDOWN_TASK_TIMEOUT >= self.performance.SHUTDOWN_SERVER_TIMEOUT:
                raise ValueError("SHUTDOWN_TASK_TIMEOUT must be less than SHUTDOWN_SERVER_TIMEOUT")
            
            if self.core.REQUEST_TIMEOUT >= self.performance.HTTP_TIMEOUT:
                raise ValueError("REQUEST_TIMEOUT must be less than HTTP_TIMEOUT")
            
            # Validate model settings
            if self.model.DEFAULT_MAX_TOKENS > self.model.DEFAULT_CONTEXT_LENGTH:
                raise ValueError("DEFAULT_MAX_TOKENS cannot exceed DEFAULT_CONTEXT_LENGTH")
            
            # Validate network settings
            if self.network.DEFAULT_PORT < 1024 or self.network.DEFAULT_PORT > 65535:
                raise ValueError("DEFAULT_PORT must be between 1024 and 65535")
            
            return True
        except ValueError as e:
            print(f"Configuration validation error: {e}")
            return False
    
    def get_timeout_summary(self) -> Dict[str, float]:
        """Get a summary of all timeout values for monitoring."""
        return {
            "idle_timeout": self.performance.IDLE_TIMEOUT,
            "stream_timeout": self.performance.STREAM_TIMEOUT,
            "http_timeout": self.performance.HTTP_TIMEOUT,
            "service_start_timeout": self.performance.SERVICE_START_TIMEOUT,
            "shutdown_task_timeout": self.performance.SHUTDOWN_TASK_TIMEOUT,
            "shutdown_server_timeout": self.performance.SHUTDOWN_SERVER_TIMEOUT,
            "request_timeout": self.core.REQUEST_TIMEOUT,
            "health_check_timeout": self.core.HEALTH_CHECK_TIMEOUT,
            "download_timeout": self.network.DOWNLOAD_TIMEOUT,
        }


# Create a global config instance
config = Config()

# Validate configuration on import
if not config.validate_config():
    print("Warning: Configuration validation failed. Please check your environment variables.") 