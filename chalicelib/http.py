import logging
import urllib3

# Prevent urllib from logging things like redirects
session_logger = logging.getLogger("urllib3")
session_logger.setLevel(logging.WARNING)

session = urllib3.PoolManager()
