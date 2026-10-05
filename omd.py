from collections import Counter
"""Один и тот же товар может лежать на складе в Москве, в Казани
или в обоих городах.
Ниже id товаров на каждом складе.

```python
moscow = {201, 202, 203, 204}
kazan = {203, 204, 205, 206}
```

Нужно найти:

- что можно забрать в любом из двух городов
- что есть только в Москве
- что есть только в Казани
- сколько разных товаров на обоих складах вместе"""

moscow = {201, 202, 203, 204}
kazan = {203, 204, 205, 206}
print(f'id, которые можно забрать в любом городе: {moscow & kazan}')
print(f'id, которые есть только в Москве: {moscow - kazan}')
print(f'id, которые есть только в Казани: {kazan - moscow}')
print(f'разные товары на обоих складах вместе: {len(kazan | moscow)}')

"""Дана история поисковых запросов: каждая строка — один введённый запрос.
Повтор в списке значит, что этот запрос ввели ещё раз.

```python
queries = [
    "чехол",
    "iphone",
    "чехол",
    "наушники",
    "iphone",
    "iphone",
    "кабель",
    "чехол",
    "iphone",
]
```

Нужно найти:

- сколько всего поисковых запросов в ленте
- сколько раз ввели каждый запрос
- какой запрос вводили чаще всего
- какую долю всех поисков он занимает
- какие запросы встретились один раз"""

queries = [
    "чехол",
    "iphone",
    "чехол",
    "наушники",
    "iphone",
    "iphone",
    "кабель",
    "чехол",
    "iphone",
]

print(f'в поисковой ленте {len(queries)} запросов')
print(
    *[f'поисковой запрос {i} искали {Counter(queries)[i]} раз'
      if Counter(queries)[i] not in [2, 3, 4]
      else f'поисковой запрос {i} искали {Counter(queries)[i]} раза'
      for i in Counter(queries)], sep='\n')
print(f'чаще всего вводили {max(Counter(queries).items(),
                                key=lambda x: x[1])[0]}')
print(f'самый популярный запрос составляет '
      f'{round(max(Counter(queries).items(),
                   key=lambda x: x[1])[1] / len(queries), 4)}')
not_poular_request = ', '.join(list(map(lambda x: x[0],
                                        filter(lambda x: x[1] == 1,
                                               Counter(queries).items()))))
print(f'запросы, которые встретились 1 раз: {not_poular_request}')

"""Есть список заказов:
- `status` -  статус заказа
  - `delivered` доставлен покупателю
  - `returned` возврат
- `amount` — сумма заказа.

```python
orders = [
    {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
    {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
    {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
    {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
    {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
    {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
]
```

Нужно найти:

- на какую сумму оформили возвраты
- кто хотя бы раз вернул заказ
- сколько заказов доставлено покупателю
- средний чек доставленных заказов"""

orders = [
    {"id": 1, "buyer": "anya", "status": "delivered", "amount": 900},
    {"id": 2, "buyer": "boris", "status": "returned", "amount": 4_500},
    {"id": 3, "buyer": "anya", "status": "delivered", "amount": 1_500},
    {"id": 4, "buyer": "vera", "status": "delivered", "amount": 3_200},
    {"id": 5, "buyer": "boris", "status": "delivered", "amount": 700},
    {"id": 6, "buyer": "gleb", "status": "returned", "amount": 2_100},
]

amount_return = [i['amount'] for i in orders if i['status'] == 'returned']
print(f'возврат оформили на сумму: {sum(amount_return)}')  # type: ignore

buyer_return = {i['buyer'] for i in orders if i['status'] == 'returned'}
print('покупатели:', *buyer_return, 'хотя бы раз возвращали заказ')

delivered_orders = [i for i in orders if i['status'] == 'delivered']
print(f'{len(delivered_orders)} заказов доставлено покупателю')

price_delivered_orders = [i['amount'] for i in delivered_orders]
avg = sum(price_delivered_orders) / len(price_delivered_orders)  # type: ignore
print(f'средний чек доставленных заказов составил: '
      f'{avg}')

"""Есть статистика за пять дней работы магазина.
У каждого дня число заказов, выручка и число возвратов.

```python
days = [
    {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
    {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
    {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
    {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
    {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
]
```

Нужно найти:

- выручку за всю неделю
- день с самой большой выручкой
- среднюю выручку на один заказ в каждый день
- дни, где возвратов больше 20% заказов"""

days = [
    {"day": "пн", "orders": 20, "revenue": 40_000, "returns": 2},
    {"day": "вт", "orders": 16, "revenue": 19_200, "returns": 4},
    {"day": "ср", "orders": 25, "revenue": 55_000, "returns": 1},
    {"day": "чт", "orders": 10, "revenue": 12_000, "returns": 3},
    {"day": "пт", "orders": 30, "revenue": 48_000, "returns": 3},
]

revenue_days = [i['revenue'] for i in days]
print(f'выручка за неделю составила: {sum(revenue_days)}')  # type: ignore

print(f'день с самой большой выручкой: '
      f'{max(days, key=lambda x: x["revenue"])["day"]}')  # type: ignore

mean_revenue_days = {i['day']: i['revenue'] / i['orders']  # type: ignore
                     for i in days}
for i in mean_revenue_days:
    print(f'средняя выручка в {i} составила {mean_revenue_days[i]}')


many_returns = ', '.join(i['day'] for i in days  # type: ignore
                         if i['returns'] / i['orders'] > 0.2  # type: ignore
                         )  # type: ignore
print('дни, где возвратов более 20%:', many_returns)

"""Есть список отзывов на товары.
На каждой строке — по одному.
Данные слегка битые, и названия товара записаны в разном регистре.
`id` при этом один и тот же для одного и того же товара.
Перед подсчётом приведите названия к одному формату,
иначе они будут считаться как разные`.

```python
reviews = [
    {"id": 1, "product": "Чехол", "stars": 5},
    {"id": 1, "product": "Чехол", "stars": 3},
    {"id": 1, "product": "Чехол", "stars": 4},
    {"id": 2, "product": "Наушники", "stars": 2},
    {"id": 2, "product": "наушники", "stars": 2},
    {"id": 2, "product": "НАУШНИКИ", "stars": 5},
    {"id": 3, "product": "Планшет", "stars": 5},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 5, "product": "Кабель", "stars": 1},
]
```

Нужно найти:

- среднюю оценку каждого товара
- худший товар по средней оценке среди тех, у кого хотя бы два отзыва
- сколько отзывов на 1 или 2 звезды
- какую долю всех отзывов они составляют"""

reviews = [
    {"id": 1, "product": "Чехол", "stars": 5},
    {"id": 1, "product": "Чехол", "stars": 3},
    {"id": 1, "product": "Чехол", "stars": 4},
    {"id": 2, "product": "Наушники", "stars": 2},
    {"id": 2, "product": "наушники", "stars": 2},
    {"id": 2, "product": "НАУШНИКИ", "stars": 5},
    {"id": 3, "product": "Планшет", "stars": 5},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 4, "product": "Колонка", "stars": 4},
    {"id": 5, "product": "Кабель", "stars": 1},
]

stars: dict[str, list[int]] = {}
for i in reviews:
    if i['product'].lower() in stars:  # type: ignore
        stars[i['product'].lower()].append(i['stars'])  # type: ignore
    else:
        stars[i['product'].lower()] = [i['stars']]  # type: ignore
for i in stars:
    print(f'средняя ценка товара {i} составила '
          f'{sum(stars[i]) / len(stars[i])}')

bad_good = min(list(filter(lambda x: len(x[1]) >= 2, stars.items())),
               key=lambda x: sum(x[1]) / len(x[1]))[0]
print(f'худший товар среди тех, у кого хотя бы два отзыва {bad_good}')

count_low_stars = len(list(filter(lambda x: x['stars'] <= 2,  # type: ignore
                                  reviews)))
print(f'количество отзывов на 1 или 2 звезды составило {count_low_stars}')
