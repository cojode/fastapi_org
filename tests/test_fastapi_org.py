import pytest
from fastapi import FastAPI
from fastapi.routing import APIRoute
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_get_org_by_id_success(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        fastapi_app.url_path_for("get_org_by_id", id=1),
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["data"]["id"] == 1
    assert data["data"]["name"] == "Moscow Restaurant 1"
    assert data["data"]["building_id"] == 1
    assert "building" in data["data"]
    assert "activities" in data["data"]
    assert "phone_numbers" in data["data"]


@pytest.mark.anyio
async def test_search_org_by_name_exact_one(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={"organization_name": "Moscow Sports Center"},
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 1
    assert any(org["name"] == "Moscow Sports Center" for org in data["values"])


@pytest.mark.anyio
async def test_search_org_by_name_multiple_by_partial_name(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={"organization_name": "Moscow"},
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 3
    assert any("Moscow" in org["name"] for org in data["values"])


@pytest.mark.anyio
async def test_search_org_by_building_id(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={"building_id": 1},
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] >= 1
    assert any(org["building_id"] == 1 for org in data["values"])


@pytest.mark.anyio
async def test_search_org_by_activity_id(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={"activity_id": 1},
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] >= 1


@pytest.mark.anyio
async def test_search_org_with_recursive_activity(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={"activity_id": 1, "recursive_activity": True},
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"


@pytest.mark.anyio
async def test_search_org_by_circle_location(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={
            "location_shape": "circle",
            "center_la": 55.7558,
            "center_lo": 37.6173,
            "radius": 1000,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 3


@pytest.mark.anyio
async def test_search_org_by_circle_location_small_radius(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={
            "location_shape": "circle",
            "center_la": 55.7558,
            "center_lo": 37.6173,
            "radius": 10,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 2


@pytest.mark.anyio
async def test_search_org_by_rectangular_location(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={
            "location_shape": "rect",
            "first_la": 55.75,
            "first_lo": 37.61,
            "second_la": 55.76,
            "second_lo": 37.62,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 3


@pytest.mark.anyio
async def test_search_org_by_rectangular_location_small_area(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={
            "location_shape": "rect",
            "first_la": 55.7557,
            "first_lo": 37.6172,
            "second_la": 55.7559,
            "second_lo": 37.6174,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 3


@pytest.mark.anyio
async def test_search_org_by_rectangular_location_one_dot(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        params={
            "location_shape": "rect",
            "first_la": 55.7557,
            "first_lo": 37.6172,
            "second_la": 55.7558,
            "second_lo": 37.6173,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 2


@pytest.mark.anyio
async def test_search_building_by_circle_location(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/building",
        params={
            "location_shape": "circle",
            "center_la": 55.7558,
            "center_lo": 37.6173,
            "radius": 1000,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 2
    assert "address" in data["values"][0]
    assert "latitude" in data["values"][0]
    assert "longitude" in data["values"][0]


@pytest.mark.anyio
async def test_search_building_by_circle_location_small_radius(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/building",
        params={
            "location_shape": "circle",
            "center_la": 55.7558,
            "center_lo": 37.6173,
            "radius": 10,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    # Должны найти только здание 1 (самое центральное)
    assert data["count"] == 1


@pytest.mark.anyio
async def test_search_building_by_rectangular_location(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/building",
        params={
            "location_shape": "rect",
            "first_la": 55.75,
            "first_lo": 37.61,
            "second_la": 55.76,
            "second_lo": 37.62,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 2


@pytest.mark.anyio
async def test_search_building_by_rectangular_location_petersburg(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    """Test building search by rectangular location - Petersburg area."""
    response = await client.get(
        "/api/building",
        params={
            "location_shape": "rect",
            "first_la": 59.93,
            "first_lo": 30.33,
            "second_la": 59.94,
            "second_lo": 30.34,
        },
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 1


@pytest.mark.anyio
async def test_search_org_no_location_filters(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 4


@pytest.mark.anyio
async def test_search_building_no_location_filters(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/building",
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 3


@pytest.mark.anyio
async def test_search_org_no_params(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        "/api/org",
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["msg"] == "success"
    assert data["count"] == 4


@pytest.mark.anyio
async def test_organization_phone_numbers(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        fastapi_app.url_path_for("get_org_by_id", id=1),
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    phone_numbers = data["data"]["phone_numbers"]
    assert len(phone_numbers) == 2
    assert "+79990001111" in phone_numbers
    assert "+79990002222" in phone_numbers


@pytest.mark.anyio
async def test_organization_activities(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        fastapi_app.url_path_for("get_org_by_id", id=1),
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["data"]["activities"]) >= 1


@pytest.mark.anyio
async def test_unathorized_no_header(
    client: AsyncClient,
    fastapi_app: FastAPI,
    protected_routes: list[APIRoute],
) -> None:
    for route in protected_routes:
        response = await client.get(route.path)
        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
        ), f"Failed on {route.path}"


@pytest.mark.anyio
async def test_unauthorized_wrong_api_key(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
    protected_routes: list[APIRoute],
) -> None:
    for route in protected_routes:
        response = await client.get(
            route.path,
            headers={"X-API-Key": correct_api_key + "wrong_api_key_suffix"},
        )
        assert (
            response.status_code == status.HTTP_401_UNAUTHORIZED
        ), f"Failed on {route.path}"


@pytest.mark.anyio
async def test_authorized_correct_api_key(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
    protected_routes: list[APIRoute],
) -> None:
    for route in protected_routes:
        response = await client.get(
            route.path,
            headers={"X-API-Key": correct_api_key},
        )
        assert (
            response.status_code != status.HTTP_401_UNAUTHORIZED
        ), f"Failed on {route.path}"


@pytest.mark.anyio
async def test_get_org_by_id_bad_id_value(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    for bad_id_value in [-1, 5.5, "wrong"]:
        response = await client.get(
            fastapi_app.url_path_for("get_org_by_id", id=bad_id_value),
            headers={"X-API-Key": correct_api_key},
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), f"Validation failed with value {bad_id_value}"


@pytest.mark.anyio
async def test_get_org_by_id_not_found(
    client: AsyncClient,
    fastapi_app: FastAPI,
    correct_api_key: str,
) -> None:
    response = await client.get(
        fastapi_app.url_path_for("get_org_by_id", id=99999999),
        headers={"X-API-Key": correct_api_key},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
