from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.urllib import URLLibInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
from opentelemetry.instrumentation.pika import PikaInstrumentor
from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry_instrumentation_django_stomp import DjangoStompInstrumentor


def response_hook(span, request, response):
    response.headers["trace_id"] = format(span.context.trace_id, "032x")
    response.headers["span_id"] = format(span.context.span_id, "016x")
    inject(response.headers)


def log_hook(span, record):
    record.trace_id = record.otelTraceID
    record.span_id = record.otelSpanID
    del record.otelTraceID
    del record.otelSpanID


def instrument_app():
    provider = TracerProvider()
    trace.set_tracer_provider(provider)

    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

    DjangoInstrumentor().instrument(
        tracer_provider=provider, is_sql_commentor_enabled=True, response_hook=response_hook
    )
    Psycopg2Instrumentor().instrument(tracer_provider=provider, skip_dep_check=True, enable_commenter=True)
    LoggingInstrumentor().instrument(tracer_provider=provider, log_hook=log_hook)
    URLLibInstrumentor().instrument(tracer_provider=provider)
    URLLib3Instrumentor().instrument(tracer_provider=provider)
    RequestsInstrumentor().instrument(tracer_provider=provider)
    DjangoStompInstrumentor().instrument(tracer_provider=provider)
    PikaInstrumentor().instrument(tracer_provider=provider)
