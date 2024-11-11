from typing import Optional, Dict
from dataclasses import dataclass
from .events import event_emitter
import time

@dataclass
class GameState:
    status: str = 'offline'
    last_notified_status: str = 'offline'
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def retrieve_state(self):
        return self.status

    def update_state(self, **kwargs):
        old_state = self.retrieve_state()
        changed = False
        for key, value in kwargs.items():
            if hasattr(self, key) and getattr(self, key) != value:
                setattr(self, key, value)
                changed = True
        new_state = self.retrieve_state()
        if changed and new_state != self.last_notified_status:
            if new_state == 'online':
                self.start_time = time.time()
            elif new_state == 'offline':
                self.end_time = time.time()
            event_emitter.emit('game_state_changed', self, old_state, new_state)
            self.last_notified_status = new_state

    def get_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

@dataclass
class GameServerState:
    status: str = 'offline'
    lobby_id: Optional[str] = None
    server_owner: Optional[str] = None
    server_data: Optional[Dict] = None
    last_notified_status: str = 'offline'
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def retrieve_state(self):
        if self.status == 'offline' or self.lobby_id is None:
            return 'offline'
        else:
            return 'online'

    def update_state(self, **kwargs):
        old_state = self.retrieve_state()
        changed = False
        for key, value in kwargs.items():
            if hasattr(self, key) and getattr(self, key) != value:
                setattr(self, key, value)
                changed = True
        new_state = self.retrieve_state()
        if changed and new_state != self.last_notified_status:
            if new_state == 'online':
                self.start_time = time.time()
            elif new_state == 'offline':
                self.end_time = time.time()
            event_emitter.emit('game_server_state_changed', self, old_state, new_state)
            self.last_notified_status = new_state

    def get_duration(self):
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


game_state = GameState()
game_server_state = GameServerState()
