import pytest
from uuid import UUID
from httpx import AsyncClient
from fastapi import status

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
    # Создаем новый кошелек
    create_resp = await async_client.post(f"{PREFIX}/wallets")
    assert create_resp.status_code == status.HTTP_200_OK
    wallet_data = create_resp.json()
    wallet_id = UUID(wallet_data["id"])

    # Проверяем начальный баланс
    balance_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}")
    assert balance_resp.status_code == status.HTTP_200_OK
    assert balance_resp.json()['balance'] == 0

    # Проверяем историю операций (должна быть пустой)
    history_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}/operations")
    assert history_resp.status_code == status.HTTP_200_OK
    assert history_resp.json() == []


# Тест 2: Успешные операции депозита и снятия средств
@pytest.mark.anyio
async def test_successful_deposit_and_withdraw(async_client: AsyncClient):
    # Создаем кошелек
    create_resp = await async_client.post(f"{PREFIX}/wallets")
    wallet_id = UUID(create_resp.json()["id"])

    # Выполняем депозит
    deposit_resp = await async_client.put(
        f"{PREFIX}/wallets/{wallet_id}/operation",
        json=TEST_DEPOSIT.model_dump(),
    )
    assert deposit_resp.status_code == status.HTTP_200_OK
    assert deposit_resp.json()["new_wallet_balance"] == TEST_AMOUNT

    # Выполняем снятие средств
    withdraw_resp = await async_client.put(
        f"{PREFIX}/wallets/{wallet_id}/operation",
        json=TEST_VALID_WITHDRAW.model_dump()
    )
    assert withdraw_resp.status_code == status.HTTP_200_OK
    expected_balance = TEST_AMOUNT - TEST_VALID_WITHDRAW.amount
    assert withdraw_resp.json()["new_wallet_balance"] == expected_balance

    # Проверяем итоговый баланс
    final_balance_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}")
    assert final_balance_resp.json()["balance"] == expected_balance

# Тест 3: Проверка ошибки при недостатке средств + получение операции
@pytest.mark.anyio
async def test_overdraft_prevention_and_operation_retrieval(async_client: AsyncClient):
    # Создаем кошелек
    create_resp = await async_client.post(f"{PREFIX}/wallets")
    wallet_id = UUID(create_resp.json()["id"])
#
#     # Пытаемся снять средства без депозита (должно вызвать ошибку)
    overdraft_resp = await async_client.put(
        f"{PREFIX}/wallets/{wallet_id}/operation",
        json=TEST_OVERDRAFT_WITHDRAW.model_dump()
    )
    assert overdraft_resp.status_code == status.HTTP_200_OK
    error_data = overdraft_resp.json()
    assert "The operation failed!!!" in error_data["message"]
    assert "Insufficient funds" in error_data["error_message"]
#
#     # Проверяем, что операция все равно сохранилась
    history_resp = await async_client.get(f"{PREFIX}/wallets/{wallet_id}/operations")
    assert history_resp.status_code == status.HTTP_200_OK
    operations = history_resp.json()
    assert len(operations) == 1
#
#     # Проверяем детали операции
    operation = operations[0]
    assert operation["operation_type"] == "WITHDRAW"
    assert operation["amount"] == TEST_OVERDRAFT_WITHDRAW.amount
#
#     # Получаем операцию по ID
    operation_id = UUID(operation["id"])
    operation_resp = await async_client.get(
        f"{PREFIX}/wallets/{wallet_id}/operation/{operation_id}"
    )
    assert operation_resp.status_code == status.HTTP_200_OK
    assert operation_resp.json()["id"] == str(operation_id)
#
#     # Проверка несуществующей операции
    invalid_operation_resp = await async_client.get(
        f"{PREFIX}/wallets/{wallet_id}/operation/{INVALID_UUID}"
    )
    assert invalid_operation_resp.status_code == status.HTTP_404_NOT_FOUND
