# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""

class TestHome:
    """Home."""

    def test_get_homepage_returns_200(self, testapp):
        """Get homepage successful."""
        # Goes to homepage
        res = testapp.get('/')
        assert res.status_code == 200
