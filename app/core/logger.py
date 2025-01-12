import logging
import sys
from typing import Optional
from pathlib import Path
from datetime import datetime
import json
from logging.handlers import RotatingFileHandler
from app.core.config import settings, EnvironmentType
from app.core.constants import LogLevel

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
            
        # Add extra fields if present
        if hasattr(record, "extra"):
            log_obj.update(record.extra)
            
        return json.dumps(log_obj)

class Logger:
    """Centralized logging configuration"""
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._configure_logger()
        return cls._instance
    
    def _configure_logger(self):
        """Configure the logger based on environment settings"""
        logger = logging.getLogger("app")
        logger.setLevel(self._get_log_level())
        
        # Clear any existing handlers
        logger.handlers = []
        
        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = self._get_formatter()
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # Add file handler in non-development environments
        if settings.ENVIRONMENT != EnvironmentType.DEVELOPMENT:
            file_handler = self._setup_file_handler()
            logger.addHandler(file_handler)
        
        self._logger = logger
    
    def _get_formatter(self) -> logging.Formatter:
        """Get the appropriate formatter based on environment"""
        if settings.ENVIRONMENT == EnvironmentType.DEVELOPMENT:
            return logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        return JSONFormatter()
    
    def _get_log_level(self) -> int:
        """Get the log level based on environment"""
        env_level = settings.LOG_LEVEL if hasattr(settings, 'LOG_LEVEL') else None
        
        if env_level:
            return getattr(logging, env_level.upper())
            
        if settings.ENVIRONMENT == EnvironmentType.DEVELOPMENT:
            return logging.DEBUG
        return logging.INFO
    
    def _setup_file_handler(self) -> RotatingFileHandler:
        """Setup rotating file handler for logging to file"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = RotatingFileHandler(
            filename=log_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(JSONFormatter())
        return file_handler
    
    @property
    def logger(self) -> logging.Logger:
        """Get the configured logger instance"""
        return self._logger
    
    def debug(self, msg: str, extra: Optional[dict] = None):
        """Log debug message"""
        self._logger.debug(msg, extra=extra)
    
    def info(self, msg: str, extra: Optional[dict] = None):
        """Log info message"""
        self._logger.info(msg, extra=extra)
    
    def warning(self, msg: str, extra: Optional[dict] = None):
        """Log warning message"""
        self._logger.warning(msg, extra=extra)
    
    def error(self, msg: str, extra: Optional[dict] = None):
        """Log error message"""
        self._logger.error(msg, extra=extra)
    
    def critical(self, msg: str, extra: Optional[dict] = None):
        """Log critical message"""
        self._logger.critical(msg, extra=extra)
    
    def exception(self, msg: str, exc_info=True, extra: Optional[dict] = None):
        """Log exception with traceback"""
        self._logger.exception(msg, exc_info=exc_info, extra=extra)

# Create a singleton instance
l = Logger()

# Export the logger instance
__all__ = ['l']