Joshua Samuel

# Challenge 9.1

## Import dependencies 
### Imports inside of main.py
* import argparse
* import sys
* from pathlib import Path
* import readline
* from textadv.engine import Game
* from textadv.world_loader import WorldError, load_world

### Imports inside of world_loader.py
* from __future__ import annotations
* import json
* from pathlib import Path
* from . import conditions
* from .model import (
    INVENTORY, Event, Exit, Extra, Item, Room, Trigger, World, in_loc, room_loc,
)
* from .parser import CANONICAL_DIRECTIONS

### Imports inside of save.py
* from __future__ import annotations
* import json
* import re
* from pathlib import Path
* from .model import GameState, World

### Imports from parser.py
* from __future__ import annotations
* import re
* from dataclasses import dataclass
* from typing import TYPE_CHECKING
* from .model import Item

### Imports from output.py
* from __future__ import annotations
* import shutil
* import textwrap
* from collections.abc import Callable

### Imports from model.py
* from __future__ import annotations
* from dataclasses import asdict, dataclass, field, fields

### Imports from engine.py
* from __future__ import annotations
* from collections.abc import Callable
* from pathlib import Path
* from . import commands
* from .conditions import apply_all, check_all
* from .model import INVENTORY, Extra, GameState, Item, World, in_loc,  room_loc
* from .output import Output, join_list
* from .parser import Command, parse

### Imports from conditions.py
* from __future__ import annotations
* from typing import TYPE_CHECKING
* from .model import INVENTORY, Condition, Effect, room_loc
* from .engine import Game

### Imports from commands.py
* from __future__ import annotations
* from collections.abc import Callable
* from dataclasses import dataclass
* from typing import TYPE_CHECKING
* from .conditions import check_all
* from .model import INVENTORY, Item, in_loc, room_loc
* from .output import join_list
* from .parser import CANONICAL_DIRECTIONS, Command
* from .save import SaveError, load_game, save_game, save_path
* from .engine import Game

## Class dependencies
### Classesinside of main.py
* constant DEFAULT_WORLD (has-a) Path
* main (has-a) ArgumentParser and Path and WorldError and Game
* 
### Classes inside of world_loader.py
* class WorldError (is-a) Exception
* func load_world (has-a) Path
    raises WorldError
    calls on build_world
* func build_world (has-a) _Builder
* class _Builder (has-a) Item and a Room
* func build return class World
* make_extras makes a class Extra
* make_item makes a claaa Item
* make_room makes a class Room with a class Exit
* make_trigger makes a class Trigger
* make_event makes a class Event

### Classes inside of save.py
* SaveError (is-a) Exception

## Data dependencies
### Data inside of main.py
* __file__
* description
* help
* world
### Data inside of world_loader.py
* data = json.load(f)
* self.problem (list) of msg
    msg is a string
* self.items (list) of Item
* self.rooms (list) of Room


# Mermaid diagram 
Yes, I used AI for this part. Yes, it reminds me of spaghetti. 

### Imports
```mermaid
flowchart TD
    main["main.py"]
    pkg_init["textadv/__init__.py"]
    world_loader["textadv.world_loader"]
    save["textadv.save"]
    parser["textadv.parser"]
    model["textadv.model"]
    engine["textadv.engine"]
    conditions["textadv.conditions"]
    commands["textadv.commands"]
    output_ext["textadv.output (external)"]

    %% Package anchor
    pkg_init -.->|package namespace| world_loader
    pkg_init -.->|package namespace| save
    pkg_init -.->|package namespace| parser
    pkg_init -.->|package namespace| model
    pkg_init -.->|package namespace| engine
    pkg_init -.->|package namespace| conditions
    pkg_init -.->|package namespace| commands

    %% Standard Library
    main --> argparse["argparse (stdlib)"]
    main --> sys["sys (stdlib)"]
    main --> pathlib["pathlib.Path (stdlib)"]
    main -.->|optional| readline["readline (stdlib)"]
    world_loader --> json["json (stdlib)"]
    world_loader --> pathlib
    save --> json
    save --> re["re (stdlib)"]
    save --> pathlib
    parser --> re
    parser --> dataclasses_p["dataclasses.dataclass (stdlib)"]
    parser --> typing_p["typing.TYPE_CHECKING (stdlib)"]
    model --> dataclasses_m["dataclasses (asdict, dataclass,\nfield, fields) (stdlib)"]
    engine --> abc_e["collections.abc.Callable (stdlib)"]
    engine --> pathlib
    conditions --> typing_c["typing.TYPE_CHECKING (stdlib)"]
    commands --> abc_c["collections.abc.Callable (stdlib)"]
    commands --> dataclasses_c["dataclasses.dataclass (stdlib)"]
    commands --> typing_cmd["typing.TYPE_CHECKING (stdlib)"]

    %% Internal Modules
    main --> engine
    main --> world_loader
    world_loader --> conditions
    world_loader --> model
    world_loader --> parser
    save --> model
    parser -.->|TYPE_CHECKING only| model
    engine --> commands
    engine --> conditions
    engine --> model
    engine --> output_ext
    engine --> parser
    conditions --> model
    conditions -.->|TYPE_CHECKING only| engine
    commands --> conditions
    commands --> model
    commands --> output_ext
    commands --> parser
    commands --> save
    commands -.->|TYPE_CHECKING only| engine
```
### Classes
```mermaid
classDiagram
    class Exception {
        <<stdlib>>
    }
    class WorldError {
        <<textadv.world_loader>>
        +list~str~ problems
    }
    class SaveError {
        <<textadv.save>>
    }
    class _Builder {
        <<textadv.world_loader>>
        +dict data
        +list~str~ problems
        +dict~str, Item~ items
        +dict~str, Room~ rooms
        +build() World
    }
    class Command {
        <<dataclass: textadv.parser>>
        +str verb
        +str~None noun
        +str~None prep
        +str~None noun2
        +Item~None item
        +Item~None item2
    }
    class Exit {
        <<dataclass: textadv.model>>
        +str target
        +list~Condition~ requires
        +str blocked
    }
    class Extra {
        <<dataclass: textadv.model>>
        +list~Condition~ requires
        +str text
    }
    class Room {
        <<dataclass: textadv.model>>
        +str id
        +str name
        +str description
        +dict~str, Exit~ exits
        +list~Extra~ extras
    }
    class Item {
        <<dataclass: textadv.model>>
        +str id
        +str name
        +str description
        +list~str~ aliases
        +bool portable
        +bool scenery
        +bool container
        +str~None text
        +str~None article
        +list~Extra~ extras
        +a_name() str
        +the_name() str
        +vocabulary() set~str~
    }
    class Trigger {
        <<dataclass: textadv.model>>
        +str id
        +list~str~ verbs
        +str~None item
        +str~None with_
        +list~Condition~ requires
        +list~Effect~ effects
        +str~None fail
        +bool once
    }
    class Event {
        <<dataclass: textadv.model>>
        +str id
        +list~Condition~ requires
        +list~Effect~ effects
        +bool once
    }
    class World {
        <<dataclass: textadv.model>>
        +str title
        +str intro
        +str start
        +dict~str, Room~ rooms
        +dict~str, Item~ items
        +list~Trigger~ triggers
        +list~Event~ events
        +dict~str, str~ initial_locations
        +set~str~ initial_open
        +dict~str, str~ synonyms
        +int max_score
        +frozenset~str~ trigger_verbs
        +new_state() GameState
    }
    class GameState {
        <<dataclass: textadv.model>>
        +str room
        +dict~str, str~ locations
        +set~str~ open
        +set~str~ flags
        +set~str~ visited
        +set~str~ fired
        +int turns
        +int score
        +bool over
        +bool won
        +to_dict() dict
        +from_dict(data) GameState
    }
    class Output {
        <<external: textadv.output>>
        +say(text)
    }
    class VerbSpec {
        <<dataclass: textadv.commands>>
        +str name
        +Handler fn
        +bool nouns
        +bool meta
        +bool allow_all
    }
    class Game {
        <<textadv.engine>>
        +World world
        +Output out
        +GameState state
        +Path save_dir
        +Item~None last_item
        +start()
        +run(read)
        +handle(line)
        +resolve_nouns(cmd, allow_all) bool
        +resolve(phrase) Item~None
        +in_scope() list~Item~
        +move_to(room_id)
        +end(message, won)
        +describe_room(full)
        +describe_item(item)
        +fire_triggers(cmd) bool
        +run_events()
    }

    Exception <|-- WorldError : is-a
    Exception <|-- SaveError : is-a
    main_py ..> Game : instantiates
    main_py ..> WorldError : catches
    _Builder --> WorldError : raises
    _Builder --> World : builds
    save_py --> SaveError : raises
    save_py ..> World : reads title/rooms/items
    save_py ..> GameState : serializes/restores
    Command o-- Item : optional resolved refs (item, item2)
    Room *-- Exit : has-a (exits)
    Room *-- Extra : has-a (extras)
    Item *-- Extra : has-a (extras)
    World *-- Room : has-a (rooms)
    World *-- Item : has-a (items)
    World *-- Trigger : has-a (triggers)
    World *-- Event : has-a (events)
    World ..> GameState : creates via new_state()
    Game *-- World : has-a (world)
    Game *-- Output : has-a (out)
    Game *-- GameState : has-a (state)
    Game o-- Item : tracks last_item
    Game ..> Command : parses & populates
    Game ..> VerbSpec : looks up via commands.VERBS
    VerbSpec o-- Game : handler receives game
    VerbSpec o-- Command : handler receives cmd
    conditions_mod ..> Game : evaluates/applies on
    conditions_mod ..> GameState : reads/mutates
    commands_mod ..> Game : executes verbs & catches SaveError
    commands_mod ..> GameState : reads/mutates locations, open, over
```
### Data
```mermaid
flowchart LR
    world_json[("data/world.json\n(title, intro, start, max_score,\nsynonyms, rooms, items,\ntriggers, events)")]
    world_obj["Static World Data\n(World: rooms, items, triggers,\nevents, initial_locations,\ninitial_open, synonyms,\nmax_score, trigger_verbs)"]
    state_obj["Mutable GameState Data\n(room, locations, open, flags,\nvisited, fired, turns, score,\nover, won)"]
    save_json[("Save JSON Files\n(<name>.json)\n{version, world, state}")]
    registries["Code Registries & Tables\n(CONDITIONS, EFFECTS, *_REFS,\nVERBS, ALIASES, Parser tables,\nCANONICAL_DIRECTIONS)"]

    world_json -->|"load_world / _Builder"| world_obj
    registries -.->|"validates keys, IDs and rules"| world_obj
    world_obj -->|"creates via new_state"| state_obj
    state_obj <-->|"save_game / load_game\n(to_dict / from_dict)"| save_json
    registries -.->|"dispatches conditions, effects,\nverbs and command parsing"| state_obj
    world_obj -->|"read by Game, commands,\nconditions and save"| state_obj
```