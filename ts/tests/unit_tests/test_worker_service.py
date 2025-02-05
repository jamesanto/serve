import logging
import os

import pytest

from ts.context import Context
from ts.service import Service
from ts.service import emit_metrics


# noinspection PyClassHasNoInit
class TestService:

    model_name = 'testmodel'
    model_dir = os.path.abspath('ts/tests/unit_tests/test_utils/')
    manifest = "testmanifest"
    data = [
        {"requestId": b"123", "parameters": [
            {"name": "xyz", "value": "abc", "contentType": "text/csv"}
        ], "data": b""}
    ]
    data_array1 = [
        {"requestId": b"123", "parameters": [
            {"name": "xyz", "value": "abc1", "contentType": "text/plain"},
            {"name": "xyz", "value": "abc2", "contentType": "text/csv"}
        ], "data": b""}
    ]
    data_array2 = [
        {"requestId": b"123", "parameters": [
            {"name": "xyz[]", "value": "abc1", "contentType": "text/plain"},
            {"name": "xyz[]", "value": "abc2", "contentType": "text/csv"}
        ], "data": b""}
    ]

    @pytest.fixture()
    def service(self, mocker):
        service = object.__new__(Service)
        service._entry_point = mocker.MagicMock(return_value=['prediction'])
        service._context = Context(self.model_name, self.model_dir, self.manifest, 1, 0, '1.0')
        return service

    def test_predict(self, service, mocker):
        create_predict_response = mocker.patch("ts.service.create_predict_response")
        service.predict(self.data)
        create_predict_response.assert_called()

    def test_with_nil_request(self, service):
        with pytest.raises(ValueError, match=r"Received invalid inputs"):
            service.retrieve_data_for_inference(None)

    def test_valid_req(self, service):
        headers, input_batch, req_to_id_map = service.retrieve_data_for_inference(self.data)
        assert headers[0].get_request_property("xyz").get("content-type") == "text/csv"
        assert input_batch[0] == {"xyz": "abc"}
        assert req_to_id_map == {0: "123"}

    def test_array_req1(self, service):
        headers, input_batch, req_to_id_map = service.retrieve_data_for_inference(self.data_array1)
        assert headers[0].get_request_property("xyz").get("content-type") == ["text/plain", "text/csv"]
        assert input_batch[0] == {"xyz": ["abc1", "abc2"]}
        assert req_to_id_map == {0: "123"}

    def test_array_req2(self, service):
        headers, input_batch, req_to_id_map = service.retrieve_data_for_inference(self.data_array2)
        assert headers[0].get_request_property("xyz").get("content-type") == ["text/plain", "text/csv"]
        assert input_batch[0] == {"xyz": ["abc1", "abc2"]}
        assert req_to_id_map == {0: "123"}


# noinspection PyClassHasNoInit
class TestEmitMetrics:

    def test_emit_metrics(self, caplog):
        caplog.set_level(logging.INFO)
        metrics = {'test_emit_metrics': True}
        emit_metrics(metrics)
        assert "[METRICS]" in caplog.text
