import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta
from pawpal_system import Pet, Task, Owner, Scheduler


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_scheduler(*tasks):
    """Return a Scheduler pre-loaded with the given tasks."""
    owner = Owner(name="Alex", available_start=8, available_end=20)
    s = Scheduler(owner)
    for t in tasks:
        s.tasks.append(t)
    return s


# ── Existing tests ─────────────────────────────────────────────────────────────

def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.is_complete == False
    task.mark_complete()
    assert task.is_complete == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Evening walk", duration_minutes=20, priority="medium"))
    assert len(pet.tasks) == 1


# ── Sorting correctness ────────────────────────────────────────────────────────

def test_sort_by_time_chronological_order():
    """Tasks come back morning → afternoon → evening regardless of insertion order."""
    evening = Task(title="Evening walk",   duration_minutes=20, priority="low",    preferred_time="evening")
    morning = Task(title="Morning feed",   duration_minutes=10, priority="high",   preferred_time="morning")
    afternoon = Task(title="Afternoon play", duration_minutes=30, priority="medium", preferred_time="afternoon")

    s = make_scheduler(evening, morning, afternoon)
    result = s.sort_by_time()

    assert [t.preferred_time for t in result] == ["morning", "afternoon", "evening"]


def test_sort_by_time_unknown_slot_falls_between_morning_and_afternoon():
    """A task with an unrecognized preferred_time (default 12) sits between morning and afternoon."""
    morning   = Task(title="Feed",  duration_minutes=10, priority="high",   preferred_time="morning")
    unknown   = Task(title="Meds",  duration_minutes=5,  priority="medium", preferred_time="noon")   # unrecognized
    afternoon = Task(title="Walk",  duration_minutes=30, priority="low",    preferred_time="afternoon")

    s = make_scheduler(afternoon, unknown, morning)
    result = s.sort_by_time()

    assert result[0].title == "Feed"
    assert result[1].title == "Meds"
    assert result[2].title == "Walk"


def test_sort_by_time_does_not_mutate_original_list():
    """sort_by_time() returns a new list; self.tasks is unchanged."""
    t1 = Task(title="Evening walk", duration_minutes=20, priority="low",  preferred_time="evening")
    t2 = Task(title="Morning feed", duration_minutes=10, priority="high", preferred_time="morning")

    s = make_scheduler(t1, t2)
    original_order = list(s.tasks)
    s.sort_by_time()

    assert s.tasks == original_order


def test_sort_by_time_empty_list():
    """sort_by_time() on an empty scheduler returns an empty list without error."""
    s = make_scheduler()
    assert s.sort_by_time() == []


# ── Recurrence logic ───────────────────────────────────────────────────────────

def test_daily_recurrence_creates_next_day_task():
    """Completing a daily task returns a new task due the following day."""
    today = date.today()
    task = Task(title="Feed Buddy", duration_minutes=10, priority="high",
                recurrence="daily", due_date=today)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.recurrence == "daily"
    assert next_task.is_complete == False


def test_weekly_recurrence_creates_task_seven_days_later():
    """Completing a weekly task returns a new task due 7 days later."""
    today = date.today()
    task = Task(title="Bath time", duration_minutes=30, priority="medium",
                recurrence="weekly", due_date=today)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(weeks=1)


def test_non_recurring_task_returns_none():
    """Completing a one-off task returns None (no follow-up task created)."""
    task = Task(title="Vet visit", duration_minutes=60, priority="high", recurrence=None)
    result = task.mark_complete()
    assert result is None


def test_recurrence_without_due_date_falls_back_to_today():
    """If due_date is unset, next occurrence is calculated from today."""
    task = Task(title="Daily meds", duration_minutes=5, priority="high", recurrence="daily")
    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_complete_task_appends_next_occurrence_to_scheduler():
    """Scheduler.complete_task() adds the new recurring task to self.tasks."""
    today = date.today()
    task = Task(title="Morning walk", duration_minutes=20, priority="medium",
                recurrence="daily", due_date=today)
    s = make_scheduler(task)

    s.complete_task(task)

    assert len(s.tasks) == 2
    assert s.tasks[1].due_date == today + timedelta(days=1)
    assert s.tasks[1].is_complete == False


def test_complete_task_non_recurring_does_not_grow_list():
    """Scheduler.complete_task() does not append anything for a non-recurring task."""
    task = Task(title="Vet visit", duration_minutes=60, priority="high")
    s = make_scheduler(task)

    s.complete_task(task)

    assert len(s.tasks) == 1


# ── Conflict detection ─────────────────────────────────────────────────────────

def test_detect_conflicts_flags_overlapping_tasks():
    """Two tasks at the same start hour should produce a conflict warning."""
    owner = Owner(name="Alex", available_start=8, available_end=20)
    s = Scheduler(owner)

    walk  = Task(title="Walk Buddy",  duration_minutes=60, priority="high",   pet_name="Buddy")
    feed  = Task(title="Feed Whiskers", duration_minutes=30, priority="medium", pet_name="Whiskers")

    # Both tasks start at hour 9 — they overlap
    s._schedule = [(walk, 9), (feed, 9)]

    warnings = s.detect_conflicts()

    assert len(warnings) == 1
    assert "Walk Buddy" in warnings[0]
    assert "Feed Whiskers" in warnings[0]


def test_detect_conflicts_no_warning_for_sequential_tasks():
    """Tasks that finish before the next one starts should not conflict."""
    owner = Owner(name="Alex", available_start=8, available_end=20)
    s = Scheduler(owner)

    walk = Task(title="Walk",  duration_minutes=60, priority="high",   pet_name="Buddy")   # 9:00–10:00
    feed = Task(title="Feed",  duration_minutes=30, priority="medium", pet_name="Buddy")   # 10:00–10:30

    s._schedule = [(walk, 9), (feed, 10)]

    warnings = s.detect_conflicts()

    assert warnings == []


def test_detect_conflicts_partial_overlap():
    """Tasks that only partially overlap (not same start) are still flagged."""
    owner = Owner(name="Alex", available_start=8, available_end=20)
    s = Scheduler(owner)

    walk = Task(title="Walk", duration_minutes=90, priority="high",   pet_name="Buddy")    # 9:00–10:30
    feed = Task(title="Feed", duration_minutes=60, priority="medium", pet_name="Whiskers") # 10:00–11:00

    s._schedule = [(walk, 9), (feed, 10)]

    warnings = s.detect_conflicts()

    assert len(warnings) == 1


def test_detect_conflicts_empty_schedule():
    """No tasks in schedule should return an empty warnings list."""
    owner = Owner(name="Alex", available_start=8, available_end=20)
    s = Scheduler(owner)
    assert s.detect_conflicts() == []


# ── Runner ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_mark_complete_changes_status,
        test_add_task_increases_pet_task_count,
        test_sort_by_time_chronological_order,
        test_sort_by_time_unknown_slot_falls_between_morning_and_afternoon,
        test_sort_by_time_does_not_mutate_original_list,
        test_sort_by_time_empty_list,
        test_daily_recurrence_creates_next_day_task,
        test_weekly_recurrence_creates_task_seven_days_later,
        test_non_recurring_task_returns_none,
        test_recurrence_without_due_date_falls_back_to_today,
        test_complete_task_appends_next_occurrence_to_scheduler,
        test_complete_task_non_recurring_does_not_grow_list,
        test_detect_conflicts_flags_overlapping_tasks,
        test_detect_conflicts_no_warning_for_sequential_tasks,
        test_detect_conflicts_partial_overlap,
        test_detect_conflicts_empty_schedule,
    ]
    for t in tests:
        t()
        print(f"PASS: {t.__name__}")
