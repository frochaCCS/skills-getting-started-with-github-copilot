from src.app import activities


def test_get_activities_returns_seeded_activities(client):
    # Arrange
    expected_activities = set(activities.keys())

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == expected_activities


def test_get_activities_returns_expected_schema(client):
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for details in data.values():
        assert required_fields.issubset(details.keys())


def test_get_activities_returns_participants_as_lists(client):
    # Arrange
    pass

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for details in data.values():
        assert isinstance(details["participants"], list)
