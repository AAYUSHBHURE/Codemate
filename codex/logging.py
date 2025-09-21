from __future__ import annotations

import logging
import logging.config
from typing import Any, Dict


DEFAULT_LOGGING_CONFIG: Dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'level': 'INFO',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


def setup_logging(config: Dict[str, Any] | None = None) -> None:
    target_config = config or DEFAULT_LOGGING_CONFIG
    logging.config.dictConfig(target_config)
    logging.getLogger(__name__).debug('Logging initialised')
