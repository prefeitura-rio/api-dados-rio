# -*- coding: utf-8 -*-
import logging


class RequireNot502(logging.Filter):
    """Filters out 502 errors."""

    def filter(self, record):
        """Returns False if the record is a 502 error."""
        return not getattr(record, "status_code", None) == 502
