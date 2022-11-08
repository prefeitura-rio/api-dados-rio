# -*- coding: utf-8 -*-
import pendulum
import pytz


def v1_deprecated():
    """
    Checks if the API version is deprecated.
    """
    # TODO: This is temporary for deprecating the v1 API automatically. Past the
    #  date, this should be hardcoded to True.
    return (
        pendulum.now(tz=pytz.timezone("America/Sao_Paulo")).date()
        > pendulum.parse("2022-12-31").date()  # noqa: W503
    )


def v1_deprecation_headers():
    """
    Returns the headers to be returned when the API version is deprecated.
    """
    return {
        "Deprecation": "2022-12-31 23:59:59",
    }
