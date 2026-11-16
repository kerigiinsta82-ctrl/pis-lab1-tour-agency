# ER-модель предметной области «Туристическая фирма»

Фирма продаёт клиентам путёвки. У клиента фиксируются ФИО, адрес и телефон.
Клиенту подбирают страну (с особенностями климата) и отель определённого класса,
обсуждают длительность пребывания и стоимость. При продаже путёвки фиксируется
дата отправления; клиенту может быть предоставлена скидка. Если клиент покупает
несколько путёвок, каждая путёвка — отдельная запись.

## Диаграмма

```mermaid
erDiagram
    CLIENT ||--o{ VOUCHER : "покупает"
    HOTEL  ||--o{ VOUCHER : "входит в"
    COUNTRY ||--o{ HOTEL  : "находится в"

    CLIENT {
        int     client_id PK
        string  last_name
        string  first_name
        string  patronymic "может отсутствовать"
        string  phone
        string  address
    }
    COUNTRY {
        int     country_id PK
        string  name
        string  climate
    }
    HOTEL {
        int     hotel_id PK
        int     country_id FK
        string  name
        int     stars "класс отеля 1..5"
    }
    VOUCHER {
        int     voucher_id PK
        int     client_id FK
        int     hotel_id FK
        date    sale_date
        date    departure_date
        int     duration_days
        decimal price
        decimal discount_percent
    }
```

## Таблицы

| Таблица | Назначение | Ключи |
|---|---|---|
| `client` | Клиенты фирмы | PK `client_id` |
| `country` | Страны и их климат | PK `country_id` |
| `hotel` | Отели (класс 1–5 звёзд) | PK `hotel_id`, FK `country_id → country` |
| `voucher` | Проданные путёвки | PK `voucher_id`, FK `client_id → client`, FK `hotel_id → hotel` |

## Обоснование 3НФ

* **1НФ** — все атрибуты атомарны: ФИО разбито на фамилию, имя и отчество,
  несколько путёвок одного клиента хранятся отдельными строками `voucher`.
* **2НФ** — во всех таблицах простой первичный ключ (суррогатный id),
  поэтому частичных зависимостей от части ключа нет.
* **3НФ** — нет транзитивных зависимостей:
  * страна путёвки не хранится в `voucher`, она определяется через `hotel.country_id`;
  * климат хранится только в `country`, а не в отеле или путёвке;
  * данные клиента не дублируются в путёвке — только внешний ключ `client_id`.
