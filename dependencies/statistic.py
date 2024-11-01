from create_bot import database


# Обновление кол-ва запросов
async def update_requests_count():
    requests_all = int(ms.read(1, "stat", "requests_all")) + 1
    requests_today = int(ms.read(1, "stat", "requests_today")) + 1

    ms.update(1, "stat", "requests_all", requests_all)
    ms.update(1, "stat", "requests_today", requests_today)
