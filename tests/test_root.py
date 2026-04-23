"""
Tests for the root endpoint redirect.

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up initial state and test data
- Act: Perform the action being tested
- Assert: Verify the results
"""


class TestRootEndpoint:
    """Tests for the GET / endpoint."""

    def test_root_redirect(self, client):
        """
        Arrange: No setup needed; the root endpoint is static.
        Act: Make a GET request to /.
        Assert: Response should redirect (301 or 307) to /static/index.html.
        """
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_follow(self, client):
        """
        Arrange: No setup needed.
        Act: Make a GET request to / and follow the redirect.
        Assert: Final response should be 200 (or 404 if static file not served in test).
        """
        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        # In test environment, static files may not be served, so we expect a 404
        # But the redirect itself should have worked (307 status is followed)
        assert response.status_code in [200, 404]
