import time
from langchain_core.callbacks import BaseCallbackHandler


class Timer(BaseCallbackHandler):
    def __init__(self):
        self.times = []
        self.start_time = None

    def on_llm_start(
        self,
        serialized,
        prompts,
        *,
        run_id,
        parent_run_id=None,
        tags=None,
        metadata=None,
        **kwargs,
    ):
        self.start_time = time.perf_counter()

    def on_llm_end(self, response, *, run_id, parent_run_id=None, tags=None, **kwargs):
        if self.start_time:
            self.times.append(time.perf_counter() - self.start_time)
            self.start_time = time.perf_counter()
