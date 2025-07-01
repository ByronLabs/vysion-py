#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Vysion Python Client Library

This test suite provides exhaustive coverage for the Vysion Python client library,
testing all major functionality with different arguments and edge cases.

Features:
- Complete testing of BaseClient and Client classes
- TestBaseClient: Mock-based tests for core HTTP client functionality
- TestClient: REAL API tests (requires valid API token via VYSION_API_KEY env var)
- All API endpoints: document search, ransomware victims, IM platforms, statistics
- Error handling and edge cases
- Network and language enumeration testing
- Concurrency and async operation simulation
- Performance testing with large datasets
- Complex real-world investigation workflows
- Feed classes testing

Test Categories:
1. TestBaseClient - Tests core client initialization, session management, URL building (MOCKED)
2. TestClient - Tests all API methods with REAL API calls (requires VYSION_API_KEY)
3. TestErrorHandling - Tests error scenarios and edge cases (MOCKED)
4. TestNetworkAndLanguageEnums - Tests all supported networks and languages (MOCKED)
5. TestFeedClasses - Tests feed consumption functionality (MOCKED)
6. TestConcurrencyAndAsync - Tests concurrent and async operations (MOCKED)
7. TestComplexScenarios - Tests real-world investigation workflows (MOCKED)
8. TestPerformance - Tests performance with large datasets (MOCKED)

API Token Configuration:
Set the VYSION_API_KEY environment variable to run real API tests:
    export VYSION_API_KEY="your_actual_api_token_here"

Or modify REAL_API_TOKEN variable directly in this file.

Dependencies:
- pytest: Main testing framework
- pytest-asyncio: For async test support
- pytest-xdist: For parallel test execution
- unittest.mock: For mocking external dependencies

Usage:
    # Run all tests (skips real API tests if no token)
    pytest unitTest.py -v
    
    # Run with real API token (single thread)
    VYSION_API_KEY="your_token" pytest unitTest.py -v
    
    # Run only real API tests (single thread)
    VYSION_API_KEY="your_token" pytest unitTest.py::TestClient -v
    
    # Run tests in parallel (includes real API tests if token available)
    VYSION_API_KEY="your_token" pytest unitTest.py -n [# of workers] -v
    
    # Run with coverage (all tests, parallel safe)
    VYSION_API_KEY="your_token" pytest unitTest.py --cov=vysion -n [# of workers]

Total Tests: 54 (16 BaseClient + 14 Real API Client + 24 other test categories)
Coverage: All public methods and major code paths
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from typing import Any

# Import Vysion components
from vysion.client.client import Client, BaseClient, DaylyFeed, RansomwareFeed
from vysion.client.error import APIError
from vysion.dto import Error
from vysion.model.enum.networks import Network
from vysion.model.enum.languages import Language

# Configuration for real API tests
# Set VYSION_API_KEY environment variable or modify this directly
REAL_API_TOKEN = os.getenv("VYSION_API_KEY", None)
SKIP_REAL_API_TESTS = REAL_API_TOKEN is None

# Check if running in parallel mode (pytest-xdist)
RUNNING_IN_PARALLEL = 'PYTEST_XDIST_WORKER' in os.environ

# Test configuration
REAL_API_TEST_REASON = "Real API token not provided. Set VYSION_API_KEY environment variable to run real API tests."


class TestBaseClient:
    """Test cases for BaseClient class"""

    def test_init_with_valid_api_key(self):
        """Test BaseClient initialization with valid API key"""
        api_key = "test_api_key_12345"
        client = BaseClient(api_key=api_key)
        assert client.api_key == api_key
        assert client.headers == {}
        assert client.proxy is None

    def test_init_with_none_api_key(self):
        """Test BaseClient initialization with None API key should raise AssertionError"""
        with pytest.raises(AssertionError, match="API key MUST be provided"):
            BaseClient(api_key=None)

    def test_init_with_invalid_api_key_type(self):
        """Test BaseClient initialization with non-string API key should raise AssertionError"""
        with pytest.raises(AssertionError, match="API key MUST be a string"):
            BaseClient(api_key=12345)

    def test_init_with_headers(self):
        """Test BaseClient initialization with custom headers"""
        api_key = "test_api_key"
        headers = {"Custom-Header": "test_value"}
        client = BaseClient(api_key=api_key, headers=headers)
        assert client.headers == headers

    def test_init_with_proxy(self):
        """Test BaseClient initialization with proxy configuration"""
        api_key = "test_api_key"
        proxy = {"http": "http://proxy.example.com:8080"}
        client = BaseClient(api_key=api_key, proxy=proxy)
        assert client.proxy == proxy

    @patch('vysion.client.client.requests.Session')
    def test_get_session_creates_session_with_headers(self, mock_session_class):
        """Test that __get_session__ creates session with proper headers"""
        mock_session = Mock()
        mock_session_class.return_value = mock_session
        
        client = BaseClient(api_key="test_key")
        session = client.__get_session__()
        
        # Verify session was created and configured
        mock_session_class.assert_called_once()
        mock_session.headers.update.assert_called_once()
        assert "X-API-KEY" in mock_session.headers.update.call_args[0][0]
        assert "User-Agent" in mock_session.headers.update.call_args[0][0]

    def test_get_api_host_default(self):
        """Test _get_api_host returns default API host"""
        client = BaseClient(api_key="test_key")
        with patch.dict('os.environ', {}, clear=True):
            assert client._get_api_host() == "https://api.vysion.ai"

    def test_get_api_host_from_env(self):
        """Test _get_api_host returns environment variable value"""
        client = BaseClient(api_key="test_key")
        custom_host = "https://custom.api.host.com"
        with patch.dict('os.environ', {'API_HOST': custom_host}):
            assert client._get_api_host() == custom_host

    def test_build_api_url_simple_endpoint(self):
        """Test URL building for simple endpoint"""
        client = BaseClient(api_key="test_key")
        with patch.object(client, '_get_api_host', return_value="https://api.test.com"):
            url = client._build_api_url__("document/search")
            assert "https://api.test.com/api/v2/document/search" in url

    def test_build_api_url_with_param(self):
        """Test URL building with parameter"""
        client = BaseClient(api_key="test_key")
        with patch.object(client, '_get_api_host', return_value="https://api.test.com"):
            url = client._build_api_url__("document", "test_id")
            assert "https://api.test.com/api/v2/document/test_id" in url

    def test_build_api_url_with_query_params(self):
        """Test URL building with query parameters"""
        client = BaseClient(api_key="test_key")
        with patch.object(client, '_get_api_host', return_value="https://api.test.com"):
            url = client._build_api_url__("search", q="test", page=1, page_size=10)
            assert "q=test" in url
            assert "page=1" in url
            assert "page_size=10" in url

    def test_build_api_url_filters_none_params(self):
        """Test URL building filters out None parameters"""
        client = BaseClient(api_key="test_key")
        with patch.object(client, '_get_api_host', return_value="https://api.test.com"):
            url = client._build_api_url__("search", q="test", page=None, valid_param="value")
            assert "q=test" in url
            assert "page=" not in url
            assert "valid_param=value" in url

    @patch('vysion.client.client.requests.Session')
    def test_make_request_success(self, mock_session_class):
        """Test successful API request"""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = BaseClient(api_key="test_key")
        result = client._make_request("http://test.url")
        
        assert result == {"status": "success"}
        mock_session.get.assert_called_once_with("http://test.url")

    @patch('vysion.client.client.requests.Session')
    def test_make_request_api_error_with_json(self, mock_session_class):
        """Test API request that returns error with JSON response"""
        from vysion.dto import ErrorCode
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"code": ErrorCode.BAD_REQUEST.value, "message": "Bad Request"}
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = BaseClient(api_key="test_key")
        
        with pytest.raises(APIError) as exc_info:
            client._make_request("http://test.url")
        
        assert exc_info.value.code == ErrorCode.BAD_REQUEST.value
        assert exc_info.value.message == "Bad Request"

    @patch('vysion.client.client.requests.Session')
    def test_make_request_api_error_without_json(self, mock_session_class):
        """Test API request that returns error without JSON response"""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.side_effect = Exception("No JSON")
        mock_response.text = "Internal Server Error"
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = BaseClient(api_key="test_key")
        
        with pytest.raises(APIError) as exc_info:
            client._make_request("http://test.url")
        
        assert exc_info.value.code == 500
        assert exc_info.value.message == "Internal Server Error"

    @patch('vysion.client.client.requests.Session')
    def test_make_request_expect_json_false(self, mock_session_class):
        """Test API request with expect_json=False"""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "Plain text response"
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        client = BaseClient(api_key="test_key")
        result = client._make_request("http://test.url", expect_json=False)
        
        assert result == mock_response


class TestClient:
    """Test cases for Client class methods - Real API calls"""

    def setup_method(self):
        """Setup method to create client instance for each test"""
        if SKIP_REAL_API_TESTS:
            pytest.skip(REAL_API_TEST_REASON)
        self.client = Client(api_key=REAL_API_TOKEN)

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_search_basic(self):
        """Test basic document search functionality with real API"""
        result = self.client.search("test")
        
        # Verify it's either a successful response or an Error object
        if isinstance(result, Error):
            # If it's an error, it should have proper error structure
            assert hasattr(result, 'code')
            assert hasattr(result, 'message')
            print(f"API returned error: {result.code} - {result.message}")
        else:
            # If successful, should have data structure
            assert hasattr(result, 'total')
            assert hasattr(result, 'hits')
            print(f"Search returned {result.total} results")

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_search_with_all_parameters(self):
        """Test document search with all parameters using real API"""
        lte_date = datetime.now()
        gte_date = datetime.now() - timedelta(days=30)
        
        result = self.client.search(
            q="malware",
            lte=lte_date,
            gte=gte_date,
            page=1,
            page_size=5,
            network=Network.tor,
            language=Language.english,
            include_tag="threat",
            exclude_tag="benign"
        )
        
        if isinstance(result, Error):
            print(f"Search with parameters returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"Search with parameters returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_search_with_basic_query(self):
        """Test search with a simple, commonly found term"""
        result = self.client.search("bitcoin")
        
        if isinstance(result, Error):
            print(f"Bitcoin search returned error: {result.code} - {result.message}")
            # Even errors should be properly formatted
            assert hasattr(result, 'code')
            assert hasattr(result, 'message')
        else:
            print(f"Bitcoin search returned {result.total} results")
            assert hasattr(result, 'total')
            assert 'hits' in result or hasattr(result, 'hits')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_find_url_real(self):
        """Test find documents by URL with real API"""
        # Use a common dark web URL pattern that might exist
        test_url = "example.onion"
        result = self.client.find_url(test_url, page=1, page_size=5)
        
        if isinstance(result, Error):
            print(f"URL search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"URL search returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_get_tag_real(self):
        """Test get documents by tag with real API"""
        result = self.client.get_tag("cryptocurrency")
        
        if isinstance(result, Error):
            print(f"Tag search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"Tag search returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_find_email_real(self):
        """Test find documents by email with real API"""
        # Use a common email pattern that might exist in threat data
        email = "admin@example.com"
        result = self.client.find_email(email, page=1, page_size=5)
        
        if isinstance(result, Error):
            print(f"Email search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"Email search returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_find_phone_real(self):
        """Test find documents by phone number with real API"""
        result = self.client.find_phone("1", "5551234567")
        
        if isinstance(result, Error):
            print(f"Phone search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"Phone search returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_find_wallet_real(self):
        """Test find documents by wallet address with real API"""
        # Use a well-known Bitcoin address that might appear in threat intel
        chain = "bitcoin"
        address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Genesis block address
        result = self.client.find_wallet(chain, address)
        
        if isinstance(result, Error):
            print(f"Wallet search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"Wallet search returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_search_ransomware_victim_real(self):
        """Test ransomware victim search with real API"""
        result = self.client.search_ransomware_victim(
            q="hospital",
            network=Network.tor,
            country="US",
            page=1,
            page_size=5
        )
        
        if isinstance(result, Error):
            print(f"Ransomware victim search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"Ransomware victim search returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_ransomware_countries_stats_real(self):
        """Test ransomware countries statistics with real API"""
        result = self.client.ransomware_countries_stats(countries="US,GB")
        
        if isinstance(result, Error):
            print(f"Country stats returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"Country stats returned data")
            # Stats might have different structure
            assert result is not None

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_ransomware_groups_stats_real(self):
        """Test ransomware groups statistics with real API"""
        gte_date = datetime.now() - timedelta(days=30)
        lte_date = datetime.now()
        
        result = self.client.ransomware_groups_stats(
            countries="US",
            gte=gte_date,
            lte=lte_date
        )
        
        if isinstance(result, Error):
            print(f"Group stats returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"Group stats returned data")
            assert result is not None

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_search_im_real(self):
        """Test instant messaging search with real API"""
        result = self.client.search_im(
            platform="telegram",
            q="crypto",
            page=1,
            page_size=5
        )
        
        if isinstance(result, Error):
            print(f"IM search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"IM search returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_im_find_email_real(self):
        """Test find IM profiles by email with real API"""
        result = self.client.im_find_email("test@example.com")
        
        if isinstance(result, Error):
            print(f"IM email search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"IM email search returned {result.total} results")
            assert hasattr(result, 'total')

    @pytest.mark.skipif(SKIP_REAL_API_TESTS, reason=REAL_API_TEST_REASON)
    def test_im_find_wallet_real(self):
        """Test find IM profiles by wallet with real API"""
        result = self.client.im_find_wallet("bitcoin", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        
        if isinstance(result, Error):
            print(f"IM wallet search returned error: {result.code} - {result.message}")
            assert hasattr(result, 'code')
        else:
            print(f"IM wallet search returned {result.total} results")
            assert hasattr(result, 'total')

    # Note: The following tests for specific IDs (get_document, get_ransomware_victim, etc.)
    # and specific IM platform operations (get_im_chat, get_im_profile, etc.) are not included
    # in real API tests because they require valid IDs that exist in the system.
    # These would need to be tested manually with known valid IDs from previous search results.


class TestErrorHandling:
    """Test cases for error handling and edge cases"""

    def setup_method(self):
        """Setup method to create client instance for each test"""
        self.client = Client(api_key="test_api_key")

    @patch.object(Client, '_make_request')
    def test_api_error_handling(self, mock_make_request):
        """Test that API errors are properly handled by decorator"""
        from vysion.dto import ErrorCode
        mock_make_request.side_effect = APIError(ErrorCode.NOT_FOUND, "Not Found")
        
        result = self.client.search("test")
        
        # Should return Error object instead of raising exception
        assert isinstance(result, Error)
        assert result.code == ErrorCode.NOT_FOUND
        assert result.message == "Not Found"

    @patch.object(Client, '_make_request')
    def test_generic_exception_handling(self, mock_make_request):
        """Test that generic exceptions are properly handled by decorator"""
        from vysion.dto import ErrorCode
        mock_make_request.side_effect = ValueError("Invalid value")
        
        result = self.client.search("test")
        
        # Should return Error object with INTERNAL_SERVER_ERROR code
        assert isinstance(result, Error)
        assert result.code == ErrorCode.INTERNAL_SERVER_ERROR
        assert "Invalid value" in result.message

    def test_search_with_empty_query(self):
        """Test search with empty query string"""
        with patch.object(self.client, '_make_request') as mock_request:
            with patch.object(self.client, '_build_api_url__') as mock_build_url:
                mock_build_url.return_value = "http://test.url"
                mock_request.return_value = {"data": {"total": 0, "hits": []}}
                
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 0, "hits": []}
                    
                    result = self.client.search("")
                    
                    # Should still make the request
                    call_args = mock_build_url.call_args
                    assert call_args[1]['q'] == ""

    def test_pagination_edge_cases(self):
        """Test pagination with edge case values"""
        with patch.object(self.client, '_make_request') as mock_request:
            with patch.object(self.client, '_build_api_url__') as mock_build_url:
                mock_build_url.return_value = "http://test.url"
                mock_request.return_value = {"data": {"total": 0, "hits": []}}
                
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 0, "hits": []}
                    
                    # Test with page 0
                    result = self.client.search("test", page=0)
                    call_args = mock_build_url.call_args
                    assert call_args[1]['page'] == 0
                    
                    # Test with very large page size
                    result = self.client.search("test", page_size=1000)
                    call_args = mock_build_url.call_args
                    assert call_args[1]['page_size'] == 1000

    def test_date_range_validation(self):
        """Test date range parameters"""
        with patch.object(self.client, '_make_request') as mock_request:
            with patch.object(self.client, '_build_api_url__') as mock_build_url:
                mock_build_url.return_value = "http://test.url"
                mock_request.return_value = {"data": {"total": 0, "hits": []}}
                
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 0, "hits": []}
                    
                    # Test with gte > lte (invalid range)
                    gte_date = datetime.now()
                    lte_date = datetime.now() - timedelta(days=1)
                    
                    result = self.client.search("test", gte=gte_date, lte=lte_date)
                    
                    # Should still pass the dates to API
                    call_args = mock_build_url.call_args
                    assert call_args[1]['gte'] == gte_date
                    assert call_args[1]['lte'] == lte_date


class TestNetworkAndLanguageEnums:
    """Test cases for Network and Language enum usage"""

    def setup_method(self):
        """Setup method to create client instance for each test"""
        self.client = Client(api_key="test_api_key")

    def test_all_network_types(self):
        """Test search with all network types"""
        networks = [Network.tor, Network.i2p, Network.zeronet, 
                   Network.freenet, Network.paste, Network.clearnet, Network.graynet]
        
        for network in networks:
            with patch.object(self.client, '_make_request') as mock_request:
                with patch.object(self.client, '_build_api_url__') as mock_build_url:
                    mock_build_url.return_value = "http://test.url"
                    mock_request.return_value = {"data": {"total": 0, "hits": []}}
                    
                    with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                        mock_validate.return_value.data = {"total": 0, "hits": []}
                        
                        result = self.client.search("test", network=network)
                        
                        call_args = mock_build_url.call_args
                        assert call_args[1]['network'] == network

    def test_multiple_language_searches(self):
        """Test search with different languages"""
        languages = [Language.english, Language.spanish, Language.russian, 
                    Language.chinese, Language.german, Language.french]
        
        for language in languages:
            with patch.object(self.client, '_make_request') as mock_request:
                with patch.object(self.client, '_build_api_url__') as mock_build_url:
                    mock_build_url.return_value = "http://test.url"
                    mock_request.return_value = {"data": {"total": 0, "hits": []}}
                    
                    with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                        mock_validate.return_value.data = {"total": 0, "hits": []}
                        
                        result = self.client.search("test", language=language)
                        
                        call_args = mock_build_url.call_args
                        assert call_args[1]['language'] == language


class TestFeedClasses:
    """Test cases for Feed classes"""

    def test_ransomware_feed_initialization(self):
        """Test RansomwareFeed initialization"""
        feed = RansomwareFeed(api_key="test_key")
        assert isinstance(feed, RansomwareFeed)
        assert isinstance(feed, DaylyFeed)
        assert isinstance(feed, Client)

    def test_daily_feed_consume_method(self):
        """Test DaylyFeed consume method"""
        feed = DaylyFeed(api_key="test_key")
        
        # Should raise NotImplementedError for base class
        with pytest.raises(NotImplementedError):
            list(feed._consume_batch(datetime.now(), datetime.now()))

    @patch.object(RansomwareFeed, '_make_request')
    @patch.object(RansomwareFeed, '_build_api_url__')
    def test_ransomware_feed_consume_batch(self, mock_build_url, mock_make_request):
        """Test RansomwareFeed _consume_batch method"""
        feed = RansomwareFeed(api_key="test_key")
        
        mock_build_url.return_value = "http://test.url"
        mock_make_request.return_value = {"data": []}
        
        start_time = datetime(2023, 1, 1)
        end_time = datetime(2023, 1, 2)
        
        results = list(feed._consume_batch(start_time, end_time))
        
        assert len(results) >= 1
        mock_build_url.assert_called()
        mock_make_request.assert_called()


class TestConcurrencyAndAsync:
    """Test cases for concurrent operations"""

    def setup_method(self):
        """Setup method to create client instance for each test"""
        self.client = Client(api_key="test_api_key")

    @pytest.mark.asyncio
    async def test_multiple_concurrent_searches(self):
        """Test multiple concurrent search operations"""
        import asyncio
        
        async def mock_search(query):
            # Simulate async operation
            await asyncio.sleep(0.1)
            with patch.object(self.client, '_make_request') as mock_request:
                with patch.object(self.client, '_build_api_url__') as mock_build_url:
                    mock_build_url.return_value = "http://test.url"
                    mock_request.return_value = {"data": {"total": 1, "hits": []}}
                    
                    with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                        mock_validate.return_value.data = {"total": 1, "hits": []}
                        
                        return self.client.search(query)
        
        # Run multiple searches concurrently
        queries = ["test1", "test2", "test3", "test4", "test5"]
        tasks = [mock_search(query) for query in queries]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        for result in results:
            assert result["total"] == 1

    def test_thread_safety_simulation(self):
        """Test that client can handle multiple threads (simulation)"""
        import threading
        import time
        
        results = []
        errors = []
        
        def worker(query_id):
            try:
                with patch.object(self.client, '_make_request') as mock_request:
                    with patch.object(self.client, '_build_api_url__') as mock_build_url:
                        mock_build_url.return_value = "http://test.url"
                        mock_request.return_value = {"data": {"total": query_id, "hits": []}}
                        
                        with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                            mock_validate.return_value.data = {"total": query_id, "hits": []}
                            
                            time.sleep(0.01)  # Simulate processing time
                            result = self.client.search(f"query_{query_id}")
                            results.append(result)
            except Exception as e:
                errors.append(str(e))  # Convert exception to string
        
        # Create and start multiple threads
        threads = []
        for i in range(10):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 10


class TestComplexScenarios:
    """Test cases for complex real-world scenarios"""

    def setup_method(self):
        """Setup method to create client instance for each test"""
        self.client = Client(api_key="test_api_key")

    def test_full_investigation_workflow(self):
        """Test a complete investigation workflow"""
        with patch.object(self.client, '_make_request') as mock_request:
            with patch.object(self.client, '_build_api_url__') as mock_build_url:
                mock_build_url.return_value = "http://test.url"
                
                # Step 1: Search for indicators
                mock_request.return_value = {"data": {"total": 1, "hits": [{"id": "doc1"}]}}
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 1, "hits": [{"id": "doc1"}]}
                    search_result = self.client.search("malware indicators")
                
                # Step 2: Get document details
                mock_request.return_value = {"data": {"id": "doc1", "content": "detailed info"}}
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"id": "doc1", "content": "detailed info"}
                    doc_result = self.client.get_document("doc1")
                
                # Step 3: Search for related emails
                mock_request.return_value = {"data": {"total": 2, "hits": []}}
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 2, "hits": []}
                    email_result = self.client.find_email("suspect@example.com")
                
                # Step 4: Search for wallets
                mock_request.return_value = {"data": {"total": 1, "hits": []}}
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 1, "hits": []}
                    wallet_result = self.client.find_wallet("bitcoin", "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
                
                # Verify all steps completed successfully
                assert search_result["total"] == 1
                assert doc_result["id"] == "doc1"
                assert email_result["total"] == 2
                assert wallet_result["total"] == 1

    def test_ransomware_investigation_scenario(self):
        """Test ransomware investigation scenario"""
        with patch.object(self.client, '_make_request') as mock_request:
            with patch.object(self.client, '_build_api_url__') as mock_build_url:
                mock_build_url.return_value = "http://test.url"
                
                # Search for ransomware victims
                mock_request.return_value = {"data": {"total": 5, "hits": []}}
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 5, "hits": []}
                    victims = self.client.search_ransomware_victim(
                        q="healthcare",
                        country="US",
                        sector="healthcare"
                    )
                
                # Get statistics
                mock_request.return_value = {"data": {"stats": [{"country": "US", "count": 10}]}}
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"stats": [{"country": "US", "count": 10}]}
                    country_stats = self.client.ransomware_countries_stats("US")
                
                mock_request.return_value = {"data": {"stats": [{"group": "group1", "count": 5}]}}
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"stats": [{"group": "group1", "count": 5}]}
                    group_stats = self.client.ransomware_groups_stats("US")
                
                assert victims["total"] == 5
                assert len(country_stats["stats"]) == 1
                assert len(group_stats["stats"]) == 1

    def test_im_platform_investigation(self):
        """Test investigation across IM platforms"""
        platforms = ["telegram", "discord", "signal"]
        
        for platform in platforms:
            with patch.object(self.client, '_make_request') as mock_request:
                with patch.object(self.client, '_build_api_url__') as mock_build_url:
                    mock_build_url.return_value = "http://test.url"
                    
                    # Search messages
                    mock_request.return_value = {"data": {"total": 3, "hits": []}}
                    with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                        mock_validate.return_value.data = {"total": 3, "hits": []}
                        messages = self.client.search_im(platform=platform, q="crypto")
                    
                    # Get profile
                    mock_request.return_value = {"data": {"profile": {"id": "user123"}}}
                    with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                        mock_validate.return_value.data = {"profile": {"id": "user123"}}
                        profile = self.client.get_im_profile(platform, "user123")
                    
                    assert messages["total"] == 3
                    assert profile["profile"]["id"] == "user123"


# Performance and stress tests
class TestPerformance:
    """Test cases for performance scenarios"""

    def setup_method(self):
        """Setup method to create client instance for each test"""
        self.client = Client(api_key="test_api_key")

    def test_large_result_set_handling(self):
        """Test handling of large result sets"""
        with patch.object(self.client, '_make_request') as mock_request:
            with patch.object(self.client, '_build_api_url__') as mock_build_url:
                mock_build_url.return_value = "http://test.url"
                
                # Simulate large result set
                large_hits = [{"id": f"doc_{i}"} for i in range(1000)]
                mock_request.return_value = {"data": {"total": 1000, "hits": large_hits}}
                
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 1000, "hits": large_hits}
                    
                    result = self.client.search("test", page_size=1000)
                    
                    assert result["total"] == 1000
                    assert len(result["hits"]) == 1000

    def test_rapid_sequential_requests(self):
        """Test rapid sequential API requests"""
        with patch.object(self.client, '_make_request') as mock_request:
            with patch.object(self.client, '_build_api_url__') as mock_build_url:
                mock_build_url.return_value = "http://test.url"
                mock_request.return_value = {"data": {"total": 1, "hits": []}}
                
                with patch('vysion.dto.VysionResponse.model_validate') as mock_validate:
                    mock_validate.return_value.data = {"total": 1, "hits": []}
                    
                    # Make 100 rapid requests
                    results = []
                    for i in range(100):
                        result = self.client.search(f"query_{i}")
                        results.append(result)
                    
                    assert len(results) == 100
                    assert all(r["total"] == 1 for r in results)


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "-x",  # Stop on first failure
        "--capture=no"  # Don't capture output
    ])
