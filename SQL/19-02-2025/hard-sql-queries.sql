-- 1️⃣ Her Müşteri İçin En Son 3 Siparişi ve Toplam Harcamalarını Listeleyin
-- Her müşterinin en son 3 siparişini (OrderDate’e göre en güncel 3 sipariş) ve bu siparişlerde harcadığı toplam tutarı gösteren bir sorgu yazın.
-- Sonuç müşteri bazında sıralanmalı ve her müşterinin sadece en son 3 siparişi görünmelidir.

select * from customers 
select * from orders 
select * from order_details

with customer_orders as(
	select c.customer_id, c.company_name, o.order_id, o.order_date,
	row_number() over (partition by c.customer_id order by o.order_date desc) as customer_order,
	(od.quantity * od.unit_price) - (od.quantity * od.unit_price)*od.discount as total_amount
	from customers c 
	inner join orders o on c.customer_id = o.customer_id
),
total_order_amount as(
	select c.customer_id, o.order_id,
	(od.quantity * od.unit_price) - (od.quantity * od.unit_price)*od.discount as total_amount
	from customers c
	inner join orders o on c.customer_id = o.customer_id
	inner join order_details od on o.order_id = od.order_id
	order by c.customer_id
)
select lto.company_name, lto.customer_id, toa.order_id, toa.total_amount 
from (select * from customer_orders where customer_order <= 3) as lto
inner join total_order_amount toa on lto.order_id = toa.order_id

WITH ranked_history AS (SELECT 
	c.company_name, 
	(od.quantity * od.unit_price) - (od.quantity * od.unit_price)*od.discount AS spent,
	o.order_date,
	ROW_NUMBER() OVER (PARTITION BY c.company_name ORDER BY o.order_date DESC) AS rank
FROM 
	customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_details od ON o.order_id = od.order_id)
SELECT 
	company_name, spent
FROM ranked_history
WHERE rank <= 3
ORDER BY company_name;

-- 2️⃣ Aynı Ürünü 3 veya Daha Fazla Kez Satın Alan Müşterileri Bulun
-- Bir müşteri eğer aynı ürünü (ProductID) 3 veya daha fazla sipariş verdiyse, bu müşteriyi ve ürünleri listeleyen bir sorgu yazın.
-- Aynı ürün bir siparişte değil, farklı siparişlerde tekrar tekrar alınmış olabilir.

select * from customers 
select * from orders 
select * from order_details
select * from products

with ordered_products as(
	select c.customer_id, o.order_id, od.product_id
	from customers c 
	inner join orders o on c.customer_id = o.customer_id
	inner join order_details od on o.order_id = od.order_id
	group by c.customer_id, o.order_id, od.product_id
	order by c.customer_id
),
ordered_products_count as(
	select o.customer_id, product_id, count(o.product_id)
	from ordered_products o
	group by o.customer_id, product_id
	order by o.customer_id	
)
select * from ordered_products_count
where ordered_products_count.count >= 3


-- 3️⃣ Bir Çalışanın 30 Gün İçinde Verdiği Siparişlerin Bir Önceki 30 Güne Göre Artış/ Azalışını Hesaplayın
-- Her çalışanın (Employees), sipariş sayısının son 30 gün içinde bir önceki 30 güne kıyasla nasıl değiştiğini hesaplayan bir sorgu yazın.
-- Çalışan bazında sipariş sayısı artış/azalış yüzdesi hesaplanmalı.

-- round(123.4567, 2) --> 123.4567, 2 ondalık basamağa yuvarlanarak 123.46 oldu, yani basamağa göre yuvarlama işlemi yapar
-- değişim yüzdesi = ((yeni değer - eski değer)/eski değer) x 100

select * from employees 
select * from orders 

with last_thirty_order as(
	select e.employee_id, e.first_name, count(e.employee_id) as last_thirty_order_count from orders o 
	inner join employees e on o.employee_id = e.employee_id
 	where order_date >= (select max(order_date) from orders) - interval '30' day
	group by e.employee_id
),
last_sixty_order as(
	select e.employee_id, e.first_name, count(e.employee_id) as last_sixty_order_count from orders o
	inner join employees e on o.employee_id = e.employee_id
	where order_date <= (select max(order_date) from orders) - interval '31' day
	and order_date >= (select max(order_date) from orders) - interval '60' day
	group by e.employee_id
)
select lto.first_name, lto.last_thirty_order_count, lso.last_sixty_order_count, 
round(((lto.last_thirty_order_count - lso.last_sixty_order_count) * 100.0) / lso.last_sixty_order_count, 2) as percentage_change
from last_thirty_order lto 
inner join last_sixty_order lso on lto.employee_id = lso.employee_id


-- 4️⃣ Her Müşterinin Siparişlerinde Kullanılan İndirim Oranının Zaman İçinde Nasıl Değiştiğini Bulun
-- Müşterilerin siparişlerinde uygulanan indirim oranlarının zaman içindeki trendini hesaplayan bir sorgu yazın.
-- Müşteri bazında hareketli ortalama indirim oranlarını hesaplayın ve sipariş tarihine göre artış/azalış eğilimi belirleyin.

select * from customers 
select * from orders 
select * from order_details

with customer_discounts as(
	select o.customer_id, o.order_id, o.order_date, od.discount from orders o
	inner join order_details od on o.order_id = od.order_id
	group by o.order_id, o.order_date, od.discount
	order by o.customer_id, o.order_date
),
discount_rate as(
	select cd.customer_id, cd.order_id, cd.order_date, cd.discount,
	case 
		when lag(cd.discount) over (order by cd.order_date)  is null then 'first discount'
		when cd.discount > lag(cd.discount) over (order by cd.order_date) then 'increasing discount'
		when cd.discount < lag(cd.discount) over (order by cd.order_date) then 'decreasing discount'
		else 'no change'
	end as discount_trend
	from customer_discounts cd
	where cd.discount != 0
)
select c.company_name, dr.customer_id, dr.order_id, dr.order_date, dr.discount, dr.discount_trend
from discount_rate dr
inner join customers c on dr.customer_id = c.customer_id
order by c.company_name
