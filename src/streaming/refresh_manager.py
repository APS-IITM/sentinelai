from src.streaming.stream_engine import StreamEngine


_engine = StreamEngine()


def start_streaming():

    _engine.start_stream()


def stop_streaming():

    _engine.stop_stream()