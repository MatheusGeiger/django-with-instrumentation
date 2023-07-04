import json
import logging.config

from json import JSONDecodeError
from typing import Any
from typing import Dict
from typing import List
from typing import Union


class RedactingFilter(logging.Filter):
    """
    Filtering class which will mask the value in a dict if its key is configured on "patterns". The value will be
    changed to "***".
    Example:
         Received dict:
         {
            "some_sensible_data": "1234",
            "some_normal_data": "4567"
         }
         Specified pattern:
         ["some_sensible_data"]
         Dict output on logger:
         {
            "some_sensible_data": "***",
            "some_normal_data": "4567"
         }
    In order to use this filtering class the logger MUST be this way: logger.info("Payload body: %s", payload.body)
    The filtering won't work if the logger is this way: logger.info(f"Payload body: {payload.body}")
    """

    def __init__(self, patterns: List):
        super(RedactingFilter, self).__init__()
        self._patterns = patterns

    def filter(self, record) -> bool:
        record.args = self.redact(record.args)
        if isinstance(record.args, tuple):
            record.args = tuple(self.redact(arg) for arg in record.args)
        return True

    def redact(self, record_arg: Any) -> Any:
        if isinstance(record_arg, (bytes, str)):
            try:
                arg_dict = json.loads(record_arg)
            except JSONDecodeError:
                return record_arg
            else:
                record_arg = arg_dict

        if isinstance(record_arg, dict):
            record_arg = self._modify_dict(record_arg)
        return record_arg

    def _modify_dict(self, dict_to_modify: Dict) -> Dict:
        new_dict = {}
        for key, value in dict_to_modify.items():
            if isinstance(value, dict):
                new_dict[key] = self._modify_dict(value)
            elif isinstance(value, list):
                new_dict[key] = self._modify_list(value)  # type: ignore
            else:
                new_dict[key] = "***" if key in self._patterns else value
        return new_dict

    def _modify_list(self, list_to_modify: Union[List[Any], Dict[Any, Any]]) -> List:
        new_list = []
        for item in list_to_modify:
            if isinstance(item, dict):
                new_list.append(self._modify_dict(item))
            elif isinstance(item, list):
                new_list.append(self._modify_list(item))  # type: ignore
            else:
                new_list.append(item)
        return new_list
