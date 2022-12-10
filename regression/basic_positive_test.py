from pytest_schema import schema, Regex, Optional, Or


class TestStatusCode:
    assert_fail_message = "Response status code is not as expected"
    valid_user = {"name": "morpheus", "job": "leader"}

    def test_get_list_users_status_code_is_200(self, app):
        response = app.get_data("/api/users")
        assert response.status_code == 200, self.assert_fail_message

    def test_get_single_user_status_code_is_200(self, app):
        response = app.get_data("/api/users/5")
        assert response.status_code == 200, self.assert_fail_message

    def test_get_single_user_not_found_status_code_is_404(self, app):
        response = app.get_data("/api/users/125")
        assert response.status_code == 404, self.assert_fail_message

    def test_post_user_status_code_is_201(self, app):
        response = app.post_data("/api/users", self.valid_user)
        assert response.status_code == 201, self.assert_fail_message

    def test_put_user_status_code_is_200(self, app):
        response = app.put_data("/api/users/5", self.valid_user)
        assert response.status_code == 200, self.assert_fail_message

    def test_patch_user_status_code_is_200(self, app):
        response = app.patch_data("/api/users/5", self.valid_user)
        assert response.status_code == 200, self.assert_fail_message

    def test_delete_user_status_code_is_204(self, app):
        response = app.delete_data("/api/users/5")
        assert response.status_code == 204, self.assert_fail_message


class TestPayload:
    assert_fail_message = "Response structure is not according to data model"
    user_body = {"name": "morpheus", "job": "leader"}
    user_data_model = {
        "id": int,
        "email": Regex(r".*?@.*?\.[A-Za-z]{2,6}"),
        "first_name": str,
        "last_name": str,
        "avatar": str
    }
    users_data_model = [user_data_model]
    list_users_data_model = {
        "page": int,
        "per_page": int,
        "total": int,
        "total_pages": int,
        "data": users_data_model,
        "support": {
            "url": str,
            "text": str
        }
    }
    single_user_data_model = {
        "data": user_data_model,
        "support": {
            "url": str,
            "text": str
        }
    }
    new_user_data_model = {
        "name": user_body["name"],
        "job": user_body["job"],
        "id": str,
        "createdAt": str
    }
    updated_user_data_model = {
        "name": user_body["name"],
        "job": user_body["job"],
        "updatedAt": str
    }

    def test_get_list_users_schema_is_according_to_data_model(self, app):
        response = app.get_data("/api/users")
        response_body = response.json()
        assert response_body == schema(
            self.list_users_data_model), self.assert_fail_message

    def test_get_single_user_schema_is_according_to_data_model(self, app):
        response = app.get_data("/api/users/5")
        response_body = response.json()
        assert response_body == schema(
            self.single_user_data_model), self.assert_fail_message

    def test_get_single_user_not_found_schema_is_according_to_data_model(
            self, app):
        response = app.get_data("/api/users/125")
        response_body = response.json()
        assert response_body == {}, self.assert_fail_message

    def test_post_user_schema_is_according_to_data_model(self, app):
        response = app.post_data("/api/users", self.user_body)
        response_body = response.json()
        assert response_body == schema(
            self.new_user_data_model), self.assert_fail_message

    def test_put_user_schema_is_according_to_data_model(self, app):
        response = app.put_data("/api/users/5", self.user_body)
        response_body = response.json()
        assert response_body == schema(
            self.updated_user_data_model), self.assert_fail_message

    def test_patch_user_schema_is_according_to_data_model(self, app):
        response = app.patch_data("/api/users/5", self.user_body)
        response_body = response.json()
        assert response_body == schema(
            self.updated_user_data_model), self.assert_fail_message

    def test_delete_user_schema_is_according_to_data_model(self, app):
        response = app.delete_data("/api/users/5")
        response_body = response.text
        assert response_body == '', self.assert_fail_message


class TestHeaders:
    assert_fail_message = "Response headers is not as expected"
    valid_user = {"name": "morpheus", "job": "leader"}
    user_headers_schema = {
        'Date': str,
        'Content-Type': 'application/json; charset=utf-8',
        'Transfer-Encoding': 'chunked',
        'Connection': 'keep-alive',
        Optional('Set-Cookie'): str,
        'X-Powered-By': 'Express',
        'Access-Control-Allow-Origin': '*',
        'Etag': str,
        'Via': '1.1 vegur',
        'Cache-Control': str,
        'CF-Cache-Status': Or('HIT', 'MISS'),
        Optional('Age'): str,
        Optional('cf-request-id'): str,
        Optional('Expect-CT'): str,
        'Report-To': str,
        'NEL': str,
        'Vary': 'Accept-Encoding',
        'Server': 'cloudflare',
        'CF-RAY': str,
        'Content-Encoding': 'gzip'
    }

    user_not_found_headers_schema = {
        'Date': str,
        'Content-Type': 'application/json; charset=utf-8',
        'Connection': 'keep-alive',
        Optional('Set-Cookie'): str,
        'X-Powered-By': 'Express',
        'Access-Control-Allow-Origin': '*',
        'Etag': str,
        'Via': '1.1 vegur',
        'Cache-Control': str,
        'CF-Cache-Status': Or('HIT', 'EXPIRED'),
        Optional('Age'): str,
        Optional('cf-request-id'): str,
        Optional('Expect-CT'): str,
        'Report-To': str,
        'NEL': str,
        'Vary': 'Accept-Encoding',
        'Server': 'cloudflare',
        'CF-RAY': str
    }

    new_user_headers_schema = {
        'Date': str,
        'Content-Type': 'application/json; charset=utf-8',
        'Connection': 'keep-alive',
        Optional('Set-Cookie'): str,
        Optional('X-Powered-By'): 'Express',
        Optional('Access-Control-Allow-Origin'): '*',
        Optional('Etag'): str,
        Optional('Via'): '1.1 vegur',
        'CF-Cache-Status': 'DYNAMIC',
        Optional('cf-request-id'): str,
        Optional('Expect-CT'): str,
        'Report-To': str,
        'NEL': str,
        'Server': 'cloudflare',
        'CF-RAY': str
    }

    deleted_user_headers_schema = {
        'Date': str,
        'Connection': 'keep-alive',
        Optional('Set-Cookie'): str,
        'X-Powered-By': 'Express',
        'Access-Control-Allow-Origin': '*',
        'Etag': str,
        'Via': '1.1 vegur',
        'CF-Cache-Status': 'DYNAMIC',
        Optional('cf-request-id'): str,
        Optional('Expect-CT'): str,
        'Report-To': str,
        'NEL': str,
        'Server': 'cloudflare',
        'CF-RAY': str
    }

    def test_get_list_users_headers_as_expected(self, app):
        response = app.get_data("/api/users")
        assert dict(response.headers) == schema(
            self.user_headers_schema), self.assert_fail_message

    def test_get_single_user_headers_as_expected(self, app):
        response = app.get_data("/api/users/5")
        assert dict(response.headers) == schema(
            self.user_headers_schema), self.assert_fail_message

    def test_get_single_user_not_found_headers_as_expected(self, app):
        response = app.get_data("/api/users/125")
        assert dict(response.headers) == schema(
            self.user_not_found_headers_schema), self.assert_fail_message

    def test_post_user_headers_as_expected(self, app):
        response = app.post_data("/api/users", self.valid_user)
        assert dict(response.headers) == schema(
            self.new_user_headers_schema), self.assert_fail_message

    def test_put_user_headers_as_expected(self, app):
        response = app.put_data("/api/users/5", self.valid_user)
        assert dict(response.headers) == schema(
            self.new_user_headers_schema), self.assert_fail_message

    def test_patch_user_headers_as_expected(self, app):
        response = app.patch_data("/api/users/5", self.valid_user)
        assert dict(response.headers) == schema(
            self.new_user_headers_schema), self.assert_fail_message

    def test_delete_user_headers_as_expected(self, app):
        response = app.delete_data("/api/users/5")
        assert dict(response.headers) == schema(
            self.deleted_user_headers_schema), self.assert_fail_message


class TestPerformance:
    assert_fail_message = "Response time is not as expected"
    valid_user = {"name": "morpheus", "job": "leader"}
    expected_time = 1.0

    def test_get_list_user_time_as_expected(self, app):
        response = app.get_data("/api/users")
        assert response.elapsed.seconds <= self.expected_time, self.assert_fail_message

    def test_get_single_time_as_expected(self, app):
        response = app.get_data("/api/users/5")
        assert response.elapsed.seconds <= self.expected_time, self.assert_fail_message

    def test_get_single_user_time_as_expected(self, app):
        response = app.get_data("/api/users/125")
        assert response.elapsed.seconds <= self.expected_time, self.assert_fail_message

    def test_post_user_time_as_expected(self, app):
        response = app.post_data("/api/users", self.valid_user)
        assert response.elapsed.seconds <= self.expected_time, self.assert_fail_message

    def test_put_user_time_as_expected(self, app):
        response = app.put_data("/api/users/5", self.valid_user)
        assert response.elapsed.seconds <= self.expected_time, self.assert_fail_message

    def test_patch_user_time_as_expected(self, app):
        response = app.patch_data("/api/users/5", self.valid_user)
        assert response.elapsed.seconds <= self.expected_time, self.assert_fail_message

    def test_delete_user_time_as_expected(self, app):
        response = app.delete_data("/api/users/5")
        assert response.elapsed.seconds <= self.expected_time, self.assert_fail_message
