import pytest

import ray
from ray.data.exceptions import UserCodeException
from ray.tests.conftest import *  # noqa


def test_handle_debugger_exception(ray_start_regular_shared):
    def _bad(batch):
        if batch["id"] == 5:
            raise Exception("Test exception")

        return batch

    dataset = ray.data.range(8, override_num_blocks=1).map_batches(_bad)

    with pytest.raises(
        UserCodeException,
        match="Failed to process the following data block: {'id': array([5])}",
    ):
        dataset.materialize()
