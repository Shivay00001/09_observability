"""
Structured Logger - Production-grade logging with correlation IDs.
"""

import logging
import sys
from contextvars import ContextVar
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import uuid4

import structlog


# Context variable for request correlation
correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


def get_correlation_id() -> str:
    """Get current correlation ID."""
    return correlation_id_var.get() or str(uuid4())


def set_correlation_id(correlation_id: Optional[str] = None) -> str:
    """Set correlation ID for current context."""
    cid = correlation_id or str(uuid4())
    correlation_id_var.set(cid)
    return cid


def add_correlation_id(
    logger: structlog.BoundLogger,
    method_name: str,
    event_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """Add correlation ID to log event."""
    cid = get_correlation_id()
    if cid:
        event_dict["correlation_id"] = cid
    return event_dict


def add_timestamp(
    logger: structlog.BoundLogger,
    method_name: str,
    event_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """Add ISO timestamp to log event."""
    event_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"
    return event_dict


def configure_logging(
    level: str = "INFO",
    json_logs: bool = True,
    service_name: str = "app",
    environment: str = "development",
) -> None:
    """
    Configure structured logging.
    
    Args:
        level: Log level
        json_logs: Whether to output JSON logs
        service_name: Service name for logs
        environment: Environment name
    """
    # Configure structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        add_correlation_id,
        add_timestamp,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    if json_logs:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Add default context
    structlog.contextvars.bind_contextvars(
        service=service_name,
        environment=environment,
    )


def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """
    Get a configured logger.
    
    Args:
        name: Logger name
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class LoggerMiddleware:
    """ASGI middleware for request logging."""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("request")
    
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Extract or generate correlation ID
        headers = dict(scope.get("headers", []))
        correlation_id = headers.get(b"x-correlation-id", b"").decode() or str(uuid4())
        set_correlation_id(correlation_id)
        
        # Log request
        start_time = datetime.utcnow()
        
        self.logger.info(
            "request_started",
            method=scope["method"],
            path=scope["path"],
            query=scope.get("query_string", b"").decode(),
        )
        
        # Capture response status
        status_code = 500
        
        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)
        
        try:
            await self.app(scope, receive, send_wrapper)
        except Exception as e:
            self.logger.exception("request_error", error=str(e))
            raise
        finally:
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.logger.info(
                "request_completed",
                method=scope["method"],
                path=scope["path"],
                status_code=status_code,
                duration_seconds=duration,
            )
