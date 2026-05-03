"""
Simple tests for the vulnerable app.

These tests should PASS after security fixes are applied.
"""

import pytest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))


def test_imports():
    """Test that basic imports work"""
    try:
        import app
        assert app is not None
    except ImportError as e:
        pytest.skip(f"Cannot import app module: {e}")


def test_flask_version():
    """Test that Flask is installed"""
    try:
        import flask
        # After fix, flask should be 2.3.2+
        version = flask.__version__
        assert version is not None
        print(f"Flask version: {version}")
    except ImportError:
        pytest.skip("Flask not installed")


def test_pillow_version():
    """Test that Pillow is installed and updated"""
    try:
        import PIL
        version = PIL.__version__
        assert version is not None
        print(f"Pillow version: {version}")
        
        # After fixes, should be 8.1.1+
        major, minor = map(int, version.split('.')[:2])
        assert major >= 8
        if major == 8:
            assert minor >= 1
    except ImportError:
        pytest.skip("Pillow not installed")


def test_sql_injection_fixed():
    """Test that SQL injection vulnerability is fixed"""
    try:
        import app
        import inspect
        
        # Check that get_user uses parameterized queries
        source = inspect.getsource(app.get_user)
        
        # Should NOT have f-string in SQL query
        assert "f\"SELECT" not in source, "Still using f-string in SQL query!"
        assert "f'SELECT" not in source, "Still using f-string in SQL query!"
        
        # Should have parameterized query
        assert "?" in source or "%s" in source, "Not using parameterized query!"
    except ImportError as e:
        pytest.skip(f"Cannot import app module: {e}")
    except AttributeError:
        pytest.skip("get_user function not found in app module")


def test_command_injection_fixed():
    """Test that command injection is fixed"""
    try:
        import app
        import inspect
        
        # Find subprocess.run calls
        source = inspect.getsource(app)
        
        # Should use shell=False
        if "shell=True" in source:
            # Check if it's in a comment
            for line in source.split('\n'):
                if "shell=True" in line and not line.strip().startswith('#'):
                    pytest.fail("Still using shell=True!")
    except ImportError as e:
        pytest.skip(f"Cannot import app module: {e}")


def test_hardcoded_secrets_fixed():
    """Test that hardcoded secrets are removed"""
    try:
        import app
        import inspect
        
        source = inspect.getsource(app)
        
        # Check for environment variable usage
        if hasattr(app, 'AWS_ACCESS_KEY'):
            # Should be using os.getenv
            assert "os.getenv" in source, "Not using environment variables for secrets!"
            
            # Should NOT have hardcoded AKIA credentials
            assert "AKIAIOSFODNN7EXAMPLE" not in str(app.AWS_ACCESS_KEY), "Still has hardcoded AWS key!"
    except ImportError as e:
        pytest.skip(f"Cannot import app module: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])