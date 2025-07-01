select * from categories
select * from customers
select * from employees
select * from orders
select * from order_details
select * from products
select * from shippers
select * from suppliers

select * from products where category_id = 3 or category_id = 4 -- or , and operatörleri vardır
select * from products where category_id = 3 and category_id = 4
select * from products where unit_price > 56
select * from products where product_name = 'Carnarvon Tigers'
select * from products where product_name like '%ix%' -- 'ix%' ix ile başlayan, '%ix' ile biten
select * from products where product_name like '%il%x%'

select * from order_details
-- aggregates
select sum(quantity) from order_details
select sum(quantity*unit_price) from order_details
select avg(quantity*unit_price) from order_details
select max(quantity*unit_price) from order_details
select min(quantity*unit_price) from order_details
select min(quantity*unit_price) from order_details

select distinct(city) from customers
select distinct(city),company_name from customers
select distinct(city, company_name) from customers --obje döndürür

select * from customers
select city from customers group by city -- select distinct(city) from customers ile aynı sorgu
select city,count(*) from customers group by city
select city,count(*) as adet from customers group by city -- kolon ismini verdik
select city as şehir,count(*) as adet from customers group by city

-- Hangi üründen kaçar dolar satış yapmışız? (produc_id)
select product_id,sum(quantity*unit_price) as toplam from order_details group by product_id

-- Hangi personel kaçar sipariş almış? (employee_id)
select * from orders
select employee_id,count(*) from orders group by employee_id

-- Hangi tedarikçinin kaçar ürünü var? (supplier_id)
select * from products
select supplier_id,sum(units_in_stock) as ürün_miktarı from products group by supplier_id


select * from products 

-- inner join 
select * from products inner join categories
			on products.category_id = categories.category_id
-- iki tablodaki category id si aynı olan category sutunlarını product tablosuna ekledik

select products.product_id, products.product_name, categories.category_name from products inner join categories
			on products.category_id = categories.category_id


-- Hangi üründen kaçar dolar satış yapmışız? (product_name)
select products.product_id, products.product_name, sum(order_details.quantity*order_details.unit_price) as toplam from order_details 
								inner join products on products.product_id = order_details.product_id  group by products.product_id

-- Hangi personel kaçar sipariş almış? (employee_name)
select * from orders
select * from employees
select employees.employee_id, employees.first_name, count(*) from orders 
								inner join employees on employees.employee_id = orders.employee_id  group by employees.employee_id

-- Hangi tedarikçinin kaçar ürünü var? (supplier_name)
select * from products
select supplier_id, sum(units_in_stock) as ürün_miktarı from products group by supplier_id