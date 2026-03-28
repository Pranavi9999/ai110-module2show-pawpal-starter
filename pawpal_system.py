from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pet:
    name: str
    species: str  # "dog", "cat", "other"
    age: int
    preferences: list[str] = field(default_factory=list)
    tasks: list = field(default_factory=list)

    def add_task(self, task) -> None:
        """Add a Task to this pet's task list."""
        self.tasks.append(task)

    def get_species_defaults(self) -> list[str]:
        """Return default task titles recommended for this species."""
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    preferred_time: Optional[str] = None  # "morning", "afternoon", "evening"
    is_recurring: bool = False
    pet_name: Optional[str] = None  # which pet this task belongs to
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_complete = True

    def priority_value(self) -> int:
        """Return a numeric weight for sorting: high=3, medium=2, low=1."""
        pass


class Owner:
    def __init__(self, name: str, available_start: int, available_end: int):
        self.name = name
        self.available_start = available_start  # hour, e.g. 8 for 8am
        self.available_end = available_end      # hour, e.g. 20 for 8pm
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a Pet to this owner's list of pets."""
        self.pets.append(pet)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: list[Task] = []
        # Each entry is (task, assigned_start_hour) — populated by build_schedule()
        self._schedule: list[tuple[Task, int]] = []

    def add_task(self, task: Task) -> None:
        """Add a Task to the schedule."""
        pass

    def build_schedule(self) -> list[Task]:
        """Sort and place tasks within the owner's available hours; store results in self._schedule."""
        pass

    def explain_schedule(self) -> str:
        """Return a human-readable summary of scheduled tasks; requires build_schedule() first."""
        pass
