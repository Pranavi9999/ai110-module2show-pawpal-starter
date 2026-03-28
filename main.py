from pawpal_system import Owner, Pet, Task, Scheduler

# --- Setup ---
owner = Owner(name="Jordan", available_start=8, available_end=20)

mochi = Pet(name="Mochi", species="cat", age=3)
buddy = Pet(name="Buddy", species="dog", age=5)

owner.add_pet(mochi)
owner.add_pet(buddy)

# --- Tasks (different times and priorities) ---
tasks = [
    Task(title="Litter box clean", duration_minutes=10, priority="medium", preferred_time="afternoon", pet_name="Mochi"),
    Task(title="Evening walk",     duration_minutes=30, priority="high",   preferred_time="evening",   pet_name="Buddy"),
    Task(title="Breakfast feeding", duration_minutes=10, priority="high",  preferred_time="morning",   pet_name="Mochi"),
    Task(title="Playtime",         duration_minutes=20, priority="medium", preferred_time="afternoon", pet_name="Buddy"),
    Task(title="Morning walk",     duration_minutes=30, priority="high",   preferred_time="morning",   pet_name="Buddy"),
]

# --- Scheduling logic ---
PRIORITY_MAP = {"high": 3, "medium": 2, "low": 1}
TIME_ORDER   = {"morning": 8, "afternoon": 13, "evening": 17}

scheduler = Scheduler(owner)
for task in tasks:
    scheduler.tasks.append(task)

# Sort by preferred time first, then by priority (descending) within same slot
sorted_tasks = sorted(
    scheduler.tasks,
    key=lambda t: (
        TIME_ORDER.get(t.preferred_time, 12),
        -PRIORITY_MAP.get(t.priority, 1),
    ),
)

# Assign start hours using a running clock per time slot
current_hour = owner.available_start
schedule = []
for task in sorted_tasks:
    slot_start = TIME_ORDER.get(task.preferred_time, current_hour)
    start = max(current_hour, slot_start)
    end = start + task.duration_minutes / 60
    if end <= owner.available_end:
        schedule.append((task, start))
        current_hour = end

# Intentional conflict: manually inject a task at 8.0 to overlap Morning walk (8.0–8.5)
conflict_task = Task(title="Vet check-in call", duration_minutes=20, priority="high", preferred_time="morning", pet_name="Mochi")
schedule.append((conflict_task, 8.0))

scheduler._schedule = schedule

# --- Conflict Detection ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\n" + "=" * 40)
    print("  Scheduling Conflicts Detected")
    print("=" * 40)
    for warning in conflicts:
        print(f"  {warning}")

# --- Print Today's Schedule ---
print("=" * 40)
print(f"  Today's Schedule for {owner.name}")
print("=" * 40)

if not schedule:
    print("No tasks could be scheduled within available hours.")
else:
    for task, start_hour in schedule:
        h = int(start_hour)
        m = int((start_hour - h) * 60)
        time_str = f"{h:02d}:{m:02d}"
        pet_label = f"[{task.pet_name}]" if task.pet_name else ""
        print(f"  {time_str}  {task.title} {pet_label}  ({task.duration_minutes} min, {task.priority} priority)")

print("=" * 40)
print(f"  Owner available: {owner.available_start}:00 - {owner.available_end}:00")
print("=" * 40)
