import logging

from autodynatrace.sdk import sdk


def instrument_log():
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        trace_info = sdk.tracecontext_get_current()
        span_id, trace_id = trace_info.span_id, trace_info.trace_id
        record.span_id = span_id
        record.trace_id = trace_id

        return record

    logging.setLogRecordFactory(record_factory)
