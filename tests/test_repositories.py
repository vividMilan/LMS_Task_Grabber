from datetime import datetime, timedelta, timezone

from src.database.repositories import assignment_repo, course_repo, file_repo

# ==========================================
# 1. COURSE REPOSITORY TESTS
# ==========================================

def test_upsert_course_create_and_update(db):
    """Test creating a new course and updating an existing one."""
    # 1. Create a new course
    course = course_repo.upsert_course(db, course_id="EEX4532", name="Networking")
    assert course.id == "EEX4532"
    assert course.name == "Networking"
    assert course.excluded == False

    # 2. Update the existing course name
    updated_course = course_repo.upsert_course(db, course_id="EEX4532", name="Networking Advanced")
    assert course.name == "Networking Advanced"

    # Ensure no duplicates were created
    all_courses = course_repo.get_all(db)
    assert len(all_courses)


def test_toggle_course_exclusion(db):
    """Test changing the excluded flag on a course."""

    course_repo.upsert_course(db, course_id="EEX7895", name="Nueral Network")

    # toggle exclusion
    result = course_repo.toggle_exclusion(db, course_id="EEX7895", excluded=True)
    assert result == True

    saved_course = course_repo.get_by_id(db, id_val="EEX7895")
    assert saved_course.excluded == True

    # Test toggling a non-existent course returns False
    result_non_existent = course_repo.toggle_exclusion(db, course_id="INVALID", excluded=True)
    assert result_non_existent == False

# ==========================================
# 2. FILE REPOSITORY TESTS
# ==========================================

def test_add_file_if_not_exists(db):
    """Test creating a new course and updating an existing one."""
    course_repo.upsert_course(db, course_id="EEX3210", name="Discrete Math")

    # 1. First addition
    file1 = file_repo.add_if_not_exists(
        db, course_id="EEX3210", file_path="downloads/lab1.pdf", file_link="https://lms.org/lab1.pdf"
    )

    assert file1.file_path == "downloads/lab1.pdf"
    assert file1.file_link == "https://lms.org/lab1.pdf"

    # 2. Attempt duplicate addition
    file2 = file_repo.add_if_not_exists(
        db, course_id="EEX3210", file_path="downloads/lab1.pdf", file_link="https://lms.org/lab1.pdf"
    )

    assert file2.id == file1.id

    all_files = file_repo.get_all(db)
    assert len(all_files) == 1

# ==========================================
# 3. ASSIGNMENT REPOSITORY TESTS
# ==========================================

def test_upsert_and_get_upcoming_assignments(db):
    """Test creating assignments and fetching incomplete ones sorted by due date."""

    course_repo.upsert_course(db, course_id="EEX4563", name="AI Maths")

    now = datetime.now(timezone.utc)
    due_sooner = now + timedelta(days=2)
    due_later = now + timedelta(days=5)

    assignment_repo.upsert_assignment(
        db, assignment_id="A2", name="Task 2", course_id="EEX4563", link="https://lms.org/a2", due=due_later
    )
    assignment_repo.upsert_assignment(
        db, assignment_id="A1", name="Task 1", course_id="EEX4563", link="https://lms.org/a1", due=due_sooner
    )

    # 2. Fetch upcoming assignments
    upcoming = assignment_repo.get_upcoming(db)
    assert len(upcoming) == 2

    # Verify proper ascending sorting by due date (Task 1 should come before Task 2)
    assert upcoming[0].id == "A1"
    assert upcoming[1].id == "A2"

    # Verify eager loading of related course
    assert upcoming[0].course.name == "AI Maths"

def test_marks_assignment_completed(db):
    """Test marking an assignment as completed removes it from get_upcoming()."""
    course_repo.upsert_course(db, course_id="EEI3251", name="Software Engineering")

    now = datetime.now(timezone.utc)
    due = now + timedelta(days=2)

    assignment_repo.upsert_assignment(
        db, 
        assignment_id="A1", 
        name="Task 1", 
        course_id="EEI3251", 
        link="https://lms.org/a1", 
        due=due
    )

    assert len(assignment_repo.get_upcoming(db)) == 1

    success = assignment_repo.mark_completed(db, assignment_id="A1")

    assert success == True

    assert len(assignment_repo.get_upcoming(db)) == 0

# ==========================================
# 4. BASE REPOSITORY GENERIC TESTS
# ==========================================

def test_base_repository_delete(db):
    """Test generic delete functionality inherited from BaseRepository."""
    course_repo.upsert_course(db, course_id="EEX9999", name="Temp Course")

    assert course_repo.get_by_id(db, "EEX9999") is not None

    # Perform generic delete
    deleted = course_repo.delete(db, "EEX9999")
    assert deleted is True
    assert course_repo.get_by_id(db, "EEX9999") is None