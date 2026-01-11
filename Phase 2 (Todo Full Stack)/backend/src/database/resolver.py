import os
import re
from urllib.parse import urlparse
from sqlmodel import create_engine
from typing import Optional
from sqlalchemy.engine import URL


class DatabaseURLResolver:
    """
    Resolves database URL with validation and fallback mechanisms.
    """

    def __init__(self, primary_url: Optional[str] = None, fallback_to_sqlite: bool = True):
        """
        Initialize the resolver with a primary URL and fallback option.

        Args:
            primary_url: The primary database URL (e.g., PostgreSQL, MySQL)
            fallback_to_sqlite: Whether to fallback to SQLite when primary URL is invalid
        """
        self.primary_url = primary_url
        self.fallback_to_sqlite = fallback_to_sqlite

    def resolve_url(self) -> str:
        """
        Resolve the appropriate database URL based on validation and fallback rules.

        Returns:
            str: A valid database URL string
        """
        # Check if primary URL is provided and valid
        if self.primary_url:
            if self._is_valid_url(self.primary_url):
                return self.primary_url
            else:
                print(f"Warning: Primary database URL is invalid: {self.primary_url}")

        # If no primary URL or it's invalid, fallback to SQLite if enabled
        if self.fallback_to_sqlite:
            sqlite_url = self._get_default_sqlite_url()
            print(f"Falling back to SQLite database: {sqlite_url}")
            return sqlite_url

        # If no fallback is enabled and primary URL is invalid, raise an error
        raise ValueError("No valid database URL available and fallback is disabled")

    def _is_valid_url(self, url: str) -> bool:
        """
        Validate if a database URL is properly formatted.

        Args:
            url: Database URL string to validate

        Returns:
            bool: True if URL is valid, False otherwise
        """
        if not url or not isinstance(url, str) or url.strip() == "":
            return False

        try:
            # Parse the URL to check if it's well-formed
            parsed = urlparse(url.strip())

            # Check if it has a valid scheme
            if not parsed.scheme:
                return False

            # Check if it's one of the supported schemes
            supported_schemes = ['postgresql', 'postgres', 'mysql', 'sqlite']
            if parsed.scheme.lower() not in supported_schemes:
                return False

            # Additional validation for different database types
            if parsed.scheme.lower() in ['postgresql', 'postgres']:
                # For PostgreSQL, ensure host and database are provided
                if not parsed.hostname or not parsed.path.lstrip('/'):
                    return False
            elif parsed.scheme.lower() == 'mysql':
                # For MySQL, ensure host and database are provided
                if not parsed.hostname or not parsed.path.lstrip('/'):
                    return False
            elif parsed.scheme.lower() == 'sqlite':
                # For SQLite, ensure path is provided
                if not parsed.path:
                    return False

            return True
        except Exception:
            # If parsing fails, URL is invalid
            return False

    def _get_default_sqlite_url(self) -> str:
        """
        Get the default SQLite database URL suitable for container environments.

        Returns:
            str: SQLite database URL
        """
        # Use a relative path that should be writable in container environments
        return "sqlite:///./production.db"


def create_safe_engine(database_url: str, echo: bool = False):
    """
    Create a SQLAlchemy engine with safe error handling.

    Args:
        database_url: Database URL string
        echo: Whether to echo SQL statements (should be False in production)

    Returns:
        Engine: SQLAlchemy engine instance
    """
    try:
        # Validate the URL before creating the engine
        resolver = DatabaseURLResolver(database_url, fallback_to_sqlite=False)
        if not resolver._is_valid_url(database_url):
            raise ValueError(f"Invalid database URL: {database_url}")

        # Create engine with appropriate settings based on database type
        parsed = urlparse(database_url)
        connect_args = {}

        if parsed.scheme.lower() == 'sqlite':
            connect_args = {"check_same_thread": False}

        engine = create_engine(
            database_url,
            echo=echo,
            connect_args=connect_args
        )

        return engine
    except Exception as e:
        print(f"Failed to create engine with URL {database_url}: {str(e)}")
        # As a last resort, try SQLite fallback
        fallback_url = "sqlite:///./fallback.db"
        print(f"Falling back to SQLite: {fallback_url}")

        connect_args = {"check_same_thread": False}
        return create_engine(fallback_url, echo=echo, connect_args=connect_args)