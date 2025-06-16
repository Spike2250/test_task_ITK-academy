import pytest
from uuid import UUID
from decimal import Decimal
from httpx import AsyncClient
from fastapi import status
from fastapi import HTTPException
import asyncio

from .constants import (
    PREFIX,
    TEST_AMOUNT,
    TEST_DEPOSIT,
    TEST_VALID_WITHDRAW,
    TEST_OVERDRAFT_WITHDRAW,
    INVALID_UUID,
)


# Тест 1: Создание кошелька и проверка начального баланса
@pytest.mark.anyio
async def test_wallet_creation_lifecycle(async_client: AsyncClient):

    create_resp = await async_client.post(f"{PREFIX}/wallets")
    assert create_resp.status_code == status.HTTP_200_OK
    wallet_data = create_resp.json()
    wallet_id = UUID(wallet_data["id"])

    balance_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}")
    assert balance_resp.status_code == status.HTTP_200_OK
    assert balance_resp.json()['balance'] == '0.00'

    history_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}/operations")
    assert history_resp.status_code == status.HTTP_200_OK
    assert history_resp.json() == []


# Тест 2: Успешные операции депозита и снятия средств
@pytest.mark.anyio
async def test_successful_deposit_and_withdraw(async_client: AsyncClient):
    create_resp = await async_client.post(f"{PREFIX}/wallets")
    wallet_id = UUID(create_resp.json()["id"])

    # депозит
    deposit_resp = await async_client.put(
        f"{PREFIX}/wallets/{wallet_id}/operation",
        params=TEST_DEPOSIT.model_dump(mode='json'),
    )
    assert deposit_resp.status_code == status.HTTP_200_OK
    assert Decimal(
        deposit_resp.json()["new_wallet_balance"]
    ) == TEST_AMOUNT

    # снятие средств
    withdraw_resp = await async_client.put(
        f"{PREFIX}/wallets/{wallet_id}/operation",
        params=TEST_VALID_WITHDRAW.model_dump(mode="json")
    )
    assert withdraw_resp.status_code == status.HTTP_200_OK
    expected_balance = TEST_AMOUNT - TEST_VALID_WITHDRAW.amount
    assert Decimal(
        withdraw_resp.json()["new_wallet_balance"]
    ) == expected_balance

    # проверка баланса
    final_balance_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}")
    assert Decimal(
        final_balance_resp.json()["balance"]
    ) == expected_balance

    # история операций
    history_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}/operations")
    assert history_resp.status_code == status.HTTP_200_OK
    operations = history_resp.json()
    assert len(operations) == 2

    operation = operations[0]  # последняя операция (сортировка по убыванию даты)
    assert operation["operation_type"] == "WITHDRAW"
    assert Decimal(operation["amount"]) == expected_balance

    # чтение операции
    operation_id = UUID(operation["id"])
    operation_resp = await async_client.get(
        f"{PREFIX}/wallets/{wallet_id}/operation/{operation_id}"
    )
    assert operation_resp.status_code == status.HTTP_200_OK
    assert operation_resp.json()["id"] == str(operation_id)
    assert "created_at" in operation_resp.json()

    invalid_operation_resp = await async_client.get(
        f"{PREFIX}/wallets/{wallet_id}/operation/{INVALID_UUID}"
    )
    assert invalid_operation_resp.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_overdraft_prevention(async_client: AsyncClient):
    create_resp = await async_client.post(f"{PREFIX}/wallets")
    wallet_id = UUID(create_resp.json()["id"])

    # уход в "минус"
    overdraft_resp = await async_client.put(
        f"{PREFIX}/wallets/{wallet_id}/operation",
        params=TEST_OVERDRAFT_WITHDRAW.model_dump(mode="json")
    )
    assert overdraft_resp.status_code == status.HTTP_400_BAD_REQUEST
    error_data = overdraft_resp.json()
    assert "Insufficient funds" in error_data["detail"]

    # Проверяем, что операция не сохранилась
    history_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}/operations")
    assert history_resp.status_code == status.HTTP_200_OK
    operations = history_resp.json()
    assert len(operations) == 0


@pytest.mark.anyio
async def test_get_invalid_wallet(async_client: AsyncClient):
    balance_resp = await async_client.get(f"{PREFIX}/wallets/{INVALID_UUID}")
    assert balance_resp.status_code == status.HTTP_404_NOT_FOUND
    assert balance_resp.json()['detail'] == 'Wallet not found'


# # TODO: не смог разобраться с тестами на множественные запросы
# @pytest.mark.anyio
# async def test_concurrent_wallet_operations(
#     async_client: AsyncClient,
# ):
#     create_resp = await async_client.post(f"{PREFIX}/wallets")
#     wallet_id = UUID(create_resp.json()["id"])
#
#     # Количество параллельных запросов
#     num_requests = 10
#     amount = TEST_AMOUNT
#
#     # Создаем и запускаем задачи
#     tasks = [
#         async_client.post(
#             f"{PREFIX}/wallets/{wallet_id}/operations",
#             params=TEST_DEPOSIT.model_dump(mode="json")
#         )
#         for _ in range(num_requests)
#     ]
#     responses = await asyncio.gather(*tasks)
#
#     # Проверяем результаты
#     successful_operations = 0
#     for response in responses:
#         if response.status_code == 200:
#             successful_operations += 1
#         else:
#             assert response.status_code == 400
#
#     # Получаем финальный баланс
#     final_balance_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}")
#     final_balance = Decimal(
#         final_balance_resp.json()["balance"]
#     )
#
#     # Проверяем корректность баланса
#     expected_balance = successful_operations * amount
#     assert final_balance == expected_balance, (
#         f"Expected balance {expected_balance}, got {final_balance}. "
#         f"Successful operations: {successful_operations}/{num_requests}"
#     )
