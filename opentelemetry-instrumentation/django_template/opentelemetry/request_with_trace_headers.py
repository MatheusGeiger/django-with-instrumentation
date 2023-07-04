import requests

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer_provider().get_tracer(__name__)

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


with tracer.start_as_current_span("request_client"):
    headers: dict = {}
    inject(headers)
    requested = requests.post(
        data={
            "full_name": "Carl Edward Sagan",
            "given_name": "Carl",
            "family_name": "Sagan",
            "user_metadata": {"city": "santo andré", "state": "SP", "birthday": "1989-10-10", "gender": "male"},
        },
        url="http://0.0.0.0:8080/api/v1/users/attributes",
        headers=headers,
    )
