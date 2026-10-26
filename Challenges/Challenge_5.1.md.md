Joshua Samuel     
CS 361

# In-Class Challenge 5.1: Define an Interface

## Lift Motor Computer:

```python
def lift_go_up() -> None:
    pass

def lift_go_down() -> None:
    pass

def stop_lift() -> None:
    pass

def is_moving() -> bool:
    pass
```

## On-Car Computer:

### Inputs:

```python
def handle_floor_button(target_floor: int) -> None:
    # Add requested floor to stop queue
    pass

def handle_emergency_button(is_pushed: bool) -> None:
    # Trigger emergency procedures
    pass

def get_door_blocked() -> bool:
    pass

def get_floor_sensor() -> int:
    pass
```

### Outputs:

```python
def play_bell() -> None:
    pass

def display_current_floor(floor: int) -> None:
    pass

def doors_open() -> None:
    pass

def doors_close() -> None:
    pass

def emergency_alarm_activate() -> None:
    pass
```
# Intercomponent Communications

| Sender | Receiver | Method | Purpose |
|---|---|---|---|
| On-Car Computer | Lift Motor Computer | lift_go_up() | Move elevator up |
| On-Car Computer | Lift Motor Computer | lift_go_down() | Move elevator down |
| On-Car Computer | Lift Motor Computer | stop_lift() | Stop elevator |
| Lift Motor Computer | On-Car Computer | get_current_floor() | Report current floor |
| Passenger | On-Car Computer | handle_floor_button() | Request destination floor |
| Passenger | On-Car Computer | handle_emergency_button() | Trigger emergency mode |
| On-Car Computer | Doors | doors_open() | Open doors |
| On-Car Computer | Doors | doors_close() | Close doors |