from scraper.web_scraper import get_lyrics_list


def test_correctly_scrapes_lyrics_from_valid_sources(mocker):
    # Given
    valid_page_sources = [b"<html><div class='Lyrics__Container-sc-1ynbvzw-1 kUgSbL'>Lyric 1</div></html>",
                          b"<html><div class='Lyrics__Container-sc-1ynbvzw-1 kUgSbL'>Lyric 2</div></html>"]
    expected_lyrics = [["Lyric 1"], ["Lyric 2"]]

    # Mock the scrape function
    mocker.patch('scraper.web_scraper.scrape', side_effect=[["Lyric 1"], ["Lyric 2"]])

    # When
    result = get_lyrics_list(valid_page_sources)

    # Then
    assert result == expected_lyrics


def test_handles_empty_list_of_page_sources():
    # Given
    empty_page_sources = []
    expected_lyrics = []

    # When
    result = get_lyrics_list(empty_page_sources)

    # Then
    assert result == expected_lyrics


def test_manage_non_html_content(mocker):
    # Given
    page_source_list = [b'<html><body><div class="Lyrics__Container-sc-1ynbvzw-1 kUgSbL">Lyrics 1</div></body></html>',
                        b'Non-HTML content']

    expected_lyrics_list = [['Lyrics 1'], ['']]

    mocker.patch('scraper.web_scraper.scrape', side_effect=lambda x: ['Lyrics 1' if x == page_source_list[0] else ''])

    # When
    actual_lyrics_list = get_lyrics_list(page_source_list)

    # Then
    assert actual_lyrics_list == expected_lyrics_list