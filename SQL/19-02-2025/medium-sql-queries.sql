-- 1️⃣ Her Çalışanın En Çok Satış Yaptığı Ürünü Bulun
-- Her çalışanın (Employees) sattığı ürünler içinde en çok sattığı (toplam adet olarak) ürünü bulun ve sonucu çalışana göre sıralayın.

-- Common Table Expression (CTE), geçici tablo
-- PARTITION BY e.employee_id: Her çalışan için ayrı bir sıralama grubu oluşturur.
-- Her çalışana özel bir sıralama grubu oluşturur. Yani, çalışan bazında ürün sıralaması yapılmasını sağlar.
-- Her çalışanın sıralamasını kendi içinde yapmasını sağlıyor.
-- Eğer PARTITION BY kullanılmazsa, tüm veritabanındaki tüm satırları tek bir grup olarak kabul eder ve tüm veriyi tek bir liste gibi sıralar.
-- ROW_NUMBER(): Her çalışanın en çok sattığı ürüne 1, ikinci en çok sattığı ürüne 2, vb. numaralar verir.
-- ROW_NUMBER(), sonuç kümesine satır numarası atayan bir pencere fonksiyonudur.
-- Her satıra 1’den başlayarak numara verir.

select * from employees
select * from orders
select * from order_details
select * from products

WITH ranked_sales AS (
	select 
		concat(e.first_name, ' ', e.last_name) as employee_name, p.product_name, sum(od.quantity) as total_quantity,
		ROW_NUMBER() OVER (PARTITION BY e.employee_id ORDER BY SUM(od.quantity) DESC) AS rank
	from employees e
	inner join orders o on e.employee_id = o.employee_id
	inner join order_details od on o.order_id = od.order_id
	inner join products p on od.product_id = p.product_id
	group by e.employee_id, p.product_name
)
select employee_name, product_name, total_quantity
from ranked_sales
where rank = 1
order by employee_name

-- 2️⃣ Bir Ülkenin Müşterilerinin Satın Aldığı En Pahalı Ürünü Bulun
-- Belli bir ülkenin (örneğin "Germany") müşterilerinin verdiği siparişlerde satın aldığı en pahalı ürünü (UnitPrice olarak) bulun ve hangi müşterinin aldığını listeleyin.

select * from customers
select * from orders
select * from order_details
select * from products

select c.contact_name, c.country, p.product_name, od.unit_price from customers c
inner join orders o on c.customer_id = o.customer_id
inner join order_details od on o.order_id = od.order_id
inner join products p on od.product_id = p.product_id
where c.country = 'Germany' and
	od.unit_price = (
		select max(unit_price) from order_details od1
		inner join orders o1 on od1.order_id = o1.order_id
		inner join customers c1 on o1.customer_id = c1.customer_id
		where c1.country = 'Germany'
	)
order by c.contact_name

-- 3️⃣ Her Kategoride (Categories) En Çok Satış Geliri Elde Eden Ürünü Bulun
-- Her kategori için toplam satış geliri en yüksek olan ürünü bulun ve listeleyin.

select * from categories
select * from products
select * from order_details
select * from orders

with category_sale as(
	select c.category_name, p.product_name, sum(od.unit_price * od.quantity) as total_price,
	row_number() over (partition by c.category_name order by sum(od.unit_price * od.quantity) desc) as rank
	from categories c 
	inner join products p on c.category_id = p.category_id
	inner join order_details od on p.product_id = od.product_id
	inner join orders o on od.order_id = o.order_id
	group by c.category_name, p.product_name
) 
select category_name, product_name, total_price from category_sale
where rank = 1
order by category_name

-- 4️⃣ Arka Arkaya En Fazla Sipariş Veren Müşteriyi Bulun
-- Sipariş tarihleri (OrderDate) baz alınarak arka arkaya en fazla sipariş veren müşteriyi bulun. (Örneğin, bir müşteri ardışık günlerde kaç sipariş vermiş?)

-- LAG() → Önceki sipariş tarihini alır.

select * from customers
select * from orders

WITH ordered_orders AS (
	select c.contact_name, o.order_date, 
	lag(o.order_date) over (partition by c.customer_id order by o.order_date) as prev_order_date
	from customers c
	inner join orders o on c.customer_id = o.customer_id
),
streak_groups as (
    select 
        contact_name, 
        order_date, 
        prev_order_date,
        sum(case when order_date = prev_order_date + INTERVAL '1 day' then 0 else 1 end) 
        over (partition by contact_name order by order_date) as streak_group
    from ordered_orders
),
streak_counts AS (
    SELECT 
        contact_name, 
        COUNT(*) AS streak_length
    FROM streak_groups
    GROUP BY contact_name, streak_group
)
SELECT contact_name, MAX(streak_length) AS max_streak
FROM streak_counts
GROUP BY contact_name
ORDER BY max_streak DESC
LIMIT 1;


-- 5️⃣ Çalışanların Sipariş Sayısına Göre Kendi Departmanındaki Ortalamanın Üzerinde Olup Olmadığını Belirleyin
-- Her çalışanın aldığı sipariş sayısını hesaplayın ve kendi departmanındaki çalışanların ortalama sipariş sayısıyla karşılaştırın. Ortalama sipariş sayısının üstünde veya altında olduğunu belirten bir sütun ekleyin.

select * from employees
select * from orders
select * from order_details

with employee_order_count as(
	-- Her çalışanın toplam sipariş sayısını hesaplıyoruz
	select concat(e.first_name, '', e.last_name) as employee_name, 
	count(o.order_id) as order_count, e.title 
	from employees e
	inner join orders o on e.employee_id = o.employee_id
	group by e.employee_id
),
department_avg_order_count as(
	select title, avg(order_count) as avg_orders_per_department
	from employee_order_count
	group by title
)
select eoc.employee_name, eoc.order_count, eoc.title, dao.avg_orders_per_department,
case
	when eoc.order_count > dao.avg_orders_per_department then 'üstünde'
	when eoc.order_count < dao.avg_orders_per_department then 'altında'
	else 'eşit'
end as order_status
from employee_order_count eoc
inner join department_avg_order_count dao on eoc.title = dao.title
order by eoc.title, eoc.order_count desc