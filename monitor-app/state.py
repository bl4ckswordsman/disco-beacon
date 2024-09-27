from typing import Optional, Dict
from dataclasses import dataclass
from events import event_emitter

@dataclass
class ServerState:
    status: str = 'offline'
    lobby_id: Optional[str] = None
    server_owner: Optional[str] = None
    server_data: Optional[Dict] = None

    def get_state(self):
        if self.status == 'offline':
            return 'offline'
        elif self.status == 'online' and (self.server_data is None or self.lobby_id is None):
            return 'online_incomplete'
        else:
            return 'online_complete'

    def update(self, **kwargs):
        old_state = self.get_state()
        changed = False
        for key, value in kwargs.items():
            if hasattr(self, key) and getattr(self, key) != value:
                setattr(self, key, value)
                changed = True
        new_state = self.get_state()
        if changed:
            event_emitter.emit('state_changed', self, old_state, new_state)


server_state = ServerState()
