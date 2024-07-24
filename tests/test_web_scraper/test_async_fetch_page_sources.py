import pytest
from unittest.mock import patch, AsyncMock
from scraper.web_scraper import async_fetch_page_sources


@pytest.mark.asyncio
async def test_fetching_multiple_valid_urls():
    # Given
    urls = ["http://example.com", "http://example.org"]
    expected_page_sources = [b"<html>Example</html>", b"<html>Example Org</html>"]

    with patch('scraper.web_scraper.async_fetch_page_source', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.side_effect = expected_page_sources

        # When
        result = await async_fetch_page_sources(urls)

        # Then
        assert result == expected_page_sources


@pytest.mark.asyncio
async def test_handling_invalid_urls():
    # Given
    urls = ["http://invalid-url.com", "http://example.org"]
    valid_page_source = b"<html>Example Org</html>"

    with patch('scraper.web_scraper.async_fetch_page_source', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.side_effect = [Exception("Invalid URL"), valid_page_source]

        # When
        result = await async_fetch_page_sources(urls)

        # Then
        assert result == [None, valid_page_source]