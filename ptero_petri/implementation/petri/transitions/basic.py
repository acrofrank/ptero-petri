from .. import lua
from ... import rom
from ..actions.base import BasicActionBase
from ..actions.merge import BasicMergeAction
from .base import TransitionBase
from ptero_common import nicer_logging


LOG = nicer_logging.getLogger(__name__)


class BasicTransition(TransitionBase):
    ACTION_BASE_CLASS = BasicActionBase
    DEFAULT_ACTION_CLASS = BasicMergeAction

    _consume_tokens = rom.Script(lua.load('consume_tokens_basic'))

    def consume_tokens(self, enabler, color_descriptor, color_marking_key,
                       group_marking_key):

        active_tokens_key = self.active_tokens_key(color_descriptor)
        state_key = self.state_key(color_descriptor)
        arcs_in_key = self.arcs_in.key
        enablers_key = self.enablers.key

        keys = [state_key, active_tokens_key, arcs_in_key, color_marking_key,
                group_marking_key, enablers_key, self.transient_keys.key]
        args = [enabler, color_descriptor.group.idx, color_descriptor.color]

        LOG.debug("Consume tokens: KEYS=%r, ARGS=%r", keys, args)
        rv = self._consume_tokens(keys=keys, args=args)
        LOG.debug("Consume tokens returned: %r", rv)

        return rv[0]

    def state_key(self, color_descriptor):
        return self.subkey("state", color_descriptor.color)

    def active_tokens_key(self, color_descriptor):
        return self.subkey("active_tokens", color_descriptor.color)
