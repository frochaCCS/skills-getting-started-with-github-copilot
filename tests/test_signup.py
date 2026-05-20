from src.app import activities


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Debate Club"
    email = "new.student@mergington.edu"
    initial_count = len(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 1


def test_signup_rejects_duplicate_email(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup", params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_missing_activity(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_unregister_signup_cycle_succeeds(client):
    # Arrange
    activity_name = "Art Studio"
    email = "cycle.student@mergington.edu"

    # Act
    first_signup = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    unregister = client.delete(
        f"/activities/{activity_name}/signup", params={"email": email}
    )
    second_signup = client.post(
        f"/activities/{activity_name}/signup", params={"email": email}
    )

    # Assert
    assert first_signup.status_code == 200
    assert unregister.status_code == 200
    assert second_signup.status_code == 200
    assert email in activities[activity_name]["participants"]
