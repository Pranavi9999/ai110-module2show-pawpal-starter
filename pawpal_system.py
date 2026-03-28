from dataclasses import dataclass, field
from datetime import date, timedelta
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
    recurrence: Optional[str] = None  # "daily", "weekly", or None
    due_date: Optional[date] = None   # date this task is due
    pet_name: Optional[str] = None    # which pet this task belongs to
    is_complete: bool = False

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return a new Task for the next occurrence if recurring.

        Next due date is calculated as:
          - "daily"  → due_date + 1 day
          - "weekly" → due_date + 7 days
        Falls back to today if due_date is not set.
        """
        self.is_complete = True
        if self.recurrence in ("daily", "weekly"):
            base = self.due_date or date.today()
            delta = timedelta(days=1) if self.recurrence == "daily" else timedelta(weeks=1)
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                preferred_time=self.preferred_time,
                recurrence=self.recurrence,
                due_date=base + delta,
                pet_name=self.pet_name,
            )
        return None

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

    def sort_by_time(self) -> list[Task]:
        """Return tasks sorted by preferred_time slot in chronological order.

        Ordering: morning (8) → afternoon (13) → evening (17).
        Tasks with an unrecognized or missing preferred_time default to 12 (midday),
        placing them between morning and afternoon slots.

        Returns:
            A new sorted list; self.tasks is not modified.
        """
        TIME_ORDER = {"morning": 8, "afternoon": 13, "evening": 17}
        return sorted(self.tasks, key=lambda t: TIME_ORDER.get(t.preferred_time, 12))

    def filter_tasks(self, *, is_complete: Optional[bool] = None, pet_name: Optional[str] = None) -> list[Task]:
        """Return tasks filtered by completion status and/or pet name.

        Args:
            is_complete: If True, return only completed tasks. If False, only incomplete. If None, skip this filter.
            pet_name:    If provided, return only tasks belonging to that pet. If None, skip this filter.
        """
        results = self.tasks
        if is_complete is not None:
            results = [t for t in results if t.is_complete == is_complete]
        if pet_name is not None:
            results = [t for t in results if t.pet_name == pet_name]
        return results

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete and auto-schedule its next occurrence if recurring.

        Returns the newly created Task, or None if the task is not recurring.
        """
        next_task = task.mark_complete()
        if next_task is not None:
            self.tasks.append(next_task)
        return next_task

    def detect_conflicts(self) -> list[str]:
        """Check self._schedule for overlapping tasks and return a list of warning strings.

        Two tasks conflict when their time windows overlap:
            A.start < B.end  and  B.start < A.end
        Returns an empty list if no conflicts are found.
        """
        warnings = []
        entries = [(task, start, start + task.duration_minutes / 60) for task, start in self._schedule]
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                task_a, start_a, end_a = entries[i]
                task_b, start_b, end_b = entries[j]
                if start_a < end_b and start_b < end_a:
                    warnings.append(
                        f"WARNING: '{task_a.title}' ({task_a.pet_name}, "
                        f"{start_a:.2f}-{end_a:.2f}) overlaps with "
                        f"'{task_b.title}' ({task_b.pet_name}, "
                        f"{start_b:.2f}-{end_b:.2f})"
                    )
        return warnings

    def build_schedule(self) -> list[Task]:
        """Sort and place tasks within the owner's available hours; store results in self._schedule."""
        pass

    def explain_schedule(self) -> str:
        """Return a human-readable summary of scheduled tasks; requires build_schedule() first."""
        pass
