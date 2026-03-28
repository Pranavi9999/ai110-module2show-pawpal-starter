import streamlit as st
from pawpal_system import Pet, Task, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Owner & Pet Setup ---
st.subheader("Owner & Pet")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name   = st.text_input("Pet name", value="Mochi")
species    = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Set owner & pet"):
    pet = Pet(name=pet_name, species=species, age=1)
    owner = Owner(name=owner_name, available_start=8, available_end=20)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.success(f"Owner '{owner_name}' set with pet '{pet_name}'.")

if "owner" not in st.session_state:
    st.info("Set an owner and pet above to get started.")

st.divider()

# --- Add a Task ---
st.subheader("Add a Task")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

preferred_time = st.selectbox("Preferred time", ["morning", "afternoon", "evening"])

if st.button("Add task"):
    if "owner" not in st.session_state:
        st.warning("Set an owner and pet first.")
    else:
        pet = st.session_state.owner.pets[0]
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority,
            preferred_time=preferred_time,
            pet_name=pet.name,
        )
        pet.add_task(task)
        st.session_state.tasks.append(task)
        st.success(f"Added: {task_title}")

# --- Task list sorted via Scheduler.sort_by_time() ---
if st.session_state.tasks:
    if "owner" in st.session_state:
        _preview_scheduler = Scheduler(st.session_state.owner)
        _preview_scheduler.tasks = list(st.session_state.tasks)
        sorted_preview = _preview_scheduler.sort_by_time()
    else:
        sorted_preview = st.session_state.tasks

    st.caption("Tasks sorted by time slot (morning → afternoon → evening)")
    st.table([
        {
            "Time slot": t.preferred_time or "—",
            "Title": t.title,
            "Duration (min)": t.duration_minutes,
            "Priority": t.priority,
            "Pet": t.pet_name or "—",
        }
        for t in sorted_preview
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Build Schedule ---
st.subheader("Build Schedule")

PRIORITY_MAP = {"high": 3, "medium": 2, "low": 1}
TIME_ORDER   = {"morning": 8, "afternoon": 13, "evening": 17}

if st.button("Generate schedule"):
    if "owner" not in st.session_state or not st.session_state.tasks:
        st.warning("Add an owner and at least one task first.")
    else:
        owner = st.session_state.owner
        scheduler = Scheduler(owner)
        for task in st.session_state.tasks:
            scheduler.tasks.append(task)

        # Use Scheduler.sort_by_time() then break ties by priority
        sorted_tasks = sorted(
            scheduler.sort_by_time(),
            key=lambda t: (
                TIME_ORDER.get(t.preferred_time, 12),
                -PRIORITY_MAP.get(t.priority, 1),
            ),
        )

        current_hour = owner.available_start
        schedule = []
        skipped = []
        for task in sorted_tasks:
            slot_start = TIME_ORDER.get(task.preferred_time, current_hour)
            start = max(current_hour, slot_start)
            end = start + task.duration_minutes / 60
            if end <= owner.available_end:
                schedule.append((task, start))
                current_hour = end
            else:
                skipped.append(task)

        scheduler._schedule = schedule

        # --- Conflict warnings via Scheduler.detect_conflicts() ---
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.error("Schedule conflicts detected — please review before your day starts:")
            for warning in conflicts:
                # Parse out just the two task names for a pet-owner-friendly message
                # e.g. "WARNING: 'Walk' (...) overlaps with 'Feed' (...)"
                friendly = (
                    warning
                    .replace("WARNING: ", "")
                    .split("overlaps with")
                )
                if len(friendly) == 2:
                    task_a = friendly[0].split("(")[0].strip().strip("'")
                    task_b = friendly[1].split("(")[0].strip().strip("'")
                    st.warning(
                        f"**{task_a}** and **{task_b}** overlap. "
                        "Consider moving one to a different time slot or shortening its duration."
                    )
                else:
                    st.warning(warning)

        # --- Schedule table ---
        if schedule:
            st.success(f"Today's plan for {owner.name}")
            PRIORITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            st.table([
                {
                    "Start time": f"{int(s):02d}:{int((s % 1) * 60):02d}",
                    "Task": t.title,
                    "Pet": t.pet_name or "—",
                    "Duration (min)": t.duration_minutes,
                    "Priority": f"{PRIORITY_ICON.get(t.priority, '')} {t.priority}",
                }
                for t, s in schedule
            ])
        else:
            st.warning("No tasks fit within the available hours.")

        # --- Skipped tasks ---
        if skipped:
            st.error(f"{len(skipped)} task(s) couldn't fit in today's schedule:")
            for t in skipped:
                st.warning(f"**{t.title}** ({t.duration_minutes} min) — runs past {owner.available_end}:00")
