"""
Tests for FastAPI activities endpoints.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up initial state and test data
- Act: Perform the action being tested
- Assert: Verify the results
"""

import pytest


class TestGetActivities:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """
        Arrange: No setup needed; activities are pre-populated in the app.
        Act: Make a GET request to /activities.
        Assert: Response should be 200 OK with all activities.
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert len(activities) == 9  # All 9 activities


class TestSignUpForActivity:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, test_data):
        """
        Arrange: Use test data with an existing activity and new email.
        Act: Sign up the student for the activity.
        Assert: Response should be 200 OK with success message.
        """
        # Arrange
        activity = test_data["existing_activity"]
        email = test_data["new_email"]

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]

    def test_signup_activity_not_found(self, client, test_data):
        """
        Arrange: Use a nonexistent activity name and valid email.
        Act: Attempt to sign up for the nonexistent activity.
        Assert: Response should be 404 Not Found.
        """
        # Arrange
        activity = test_data["nonexistent_activity"]
        email = test_data["new_email"]

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_already_signed_up(self, client, test_data):
        """
        Arrange: Use an existing activity and an email already signed up.
        Act: Attempt to sign up the same student again.
        Assert: Response should be 400 Bad Request.
        """
        # Arrange
        activity = test_data["existing_activity"]
        email = test_data["existing_email"]  # michael@mergington.edu is already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_missing_email_parameter(self, client, test_data):
        """
        Arrange: Use an existing activity but omit the email parameter.
        Act: Attempt to sign up without providing an email.
        Assert: Response should be 422 Unprocessable Entity (FastAPI validation error).
        """
        # Arrange
        activity = test_data["existing_activity"]

        # Act
        response = client.post(f"/activities/{activity}/signup")

        # Assert
        assert response.status_code == 422  # FastAPI validation error


class TestUnregisterFromActivity:
    """Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_unregister_success(self, client, test_data):
        """
        Arrange: First sign up a student, then set up to unregister them.
        Act: Unregister the student from the activity.
        Assert: Response should be 200 OK with success message.
        """
        # Arrange
        activity = test_data["existing_activity"]
        email = test_data["new_email"]
        
        # First, sign up the student
        client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email in response.json()["message"]

    def test_unregister_activity_not_found(self, client, test_data):
        """
        Arrange: Use a nonexistent activity name.
        Act: Attempt to unregister from the nonexistent activity.
        Assert: Response should be 404 Not Found.
        """
        # Arrange
        activity = test_data["nonexistent_activity"]
        email = test_data["existing_email"]

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_student_not_signed_up(self, client, test_data):
        """
        Arrange: Use an existing activity but a student not in that activity.
        Act: Attempt to unregister a student who is not signed up.
        Assert: Response should be 400 Bad Request.
        """
        # Arrange
        activity = test_data["existing_activity"]
        email = test_data["new_email"]  # This email is not in Chess Club

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"
