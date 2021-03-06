from .storage_mixin import StorageMixin
import celery
from ptero_common import nicer_logging


LOG = nicer_logging.getLogger(__name__)


__all__ = ['NotifyTransition']


class NotifyTransition(celery.Task, StorageMixin):
    ignore_result = True

    def run(self, net_key, place_idx, transition_idx, token_idx):
        net = self.get_net(net_key)
        net.notify_transition(transition_idx, place_idx, token_idx)
