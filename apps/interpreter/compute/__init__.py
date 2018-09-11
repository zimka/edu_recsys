import logging
import pandas as pd

from apps.context.models import Directions

log = logging.getLogger(__name__)




def _reduce(result_dataframe):
    pass


def compute(diagnostics_data):
    result = {}
    global mappers
    for guid, data in diagnostics_data:
        if guid not in mappers:
            log.error("DigitalProfile.compute met unknown guid: {}".format(guid))
            continue
        current = mappers[guid](data)
        if current is not None:
            result[guid] = current
    total = pd.DataFrame(result)
    return _reduce(total)