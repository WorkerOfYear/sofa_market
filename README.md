# Основные sql запросы (для оценки стоимости)


## 1. Пользователи
* Наполнить бд тестовыми пользователями
```aiignore
INSERT INTO users (first_name, last_name, email, phone, city, hashed_password)
SELECT 
    'test_first_name', 
    'test_last_name',  
    CONCAT('test_email_', idx, '@gmail.com'),
    CONCAT('+7(111)', idx),
    'Karaganda',
    'secret_pwd'
FROM generate_series(1, 100000) as idx;
```
* Достать всех пользователей
```aiignore
SELECT * FROM Users;
```
* Достать колличество пользователей в каждом городе
```aiignore
SELECT city, COUNT(*) users_in_city FROM Users
GROUP BY city;
```

## 2. Категории
* Наполнить бд тестовыми категориями
```aiignore
INSERT INTO categories (name, slug)
SELECT 
	CONCAT('test category ', idx), 
    CONCAT('test-category-', idx)
FROM generate_series(1, 5) as idx;
```
* Достать категории
* Достать изображение категории


## 3. Продукты
* Наполнить бд тестовыми продуктами
```aiignore
INSERT INTO products (name, slug, description, price, category_id)
SELECT 
	CONCAT('test name ', idx), 
    CONCAT('test-slug', idx),  
    'some words ...',
    5000000,
	1
FROM generate_series(1, 100) as idx;
```
* Получение списка товаров
```aiignore
SELECT * FROM products ORDER BY created_at DESC LIMIT 20;
```
* Поиск товаров по категории
```aiignore
SELECT * FROM products WHERE category_id = 1 ORDER BY created_at DESC LIMIT 20;
```

### Изображения
* CRUD

### Размеры
* CRUD


## 4. Избранное
* Создать избранное для пользователе с id от 1 до 50000
```aiignore
INSERT INTO favorites (id)
SELECT generate_series(1, 50000);
```
* Добавить продукты в избранное
```aiignore
INSERT INTO favorites_products (favorite_id, product_id)
SELECT f.id, p.id
FROM favorites f
CROSS JOIN generate_series(1, 100) AS p(id);
```
* Получение всех товаров из избранного для пользователя
```aiignore
select * from favorites_products
where favorite_id = 1
```


## 5. Корзина
* CRUD
* Достать корзину для пользователя по id
* Достать товары из корзины


## 6. Покупки
* CRUD


## Сложные запросы
* Нужно выбрать всех пользователей у которых в избранном находится 2 или больше диванов
* Вывести все заказные продукты вместо с колличеством заказов
* Вывести всех пользователей которые хоть раз совершали покупку прямых диванов