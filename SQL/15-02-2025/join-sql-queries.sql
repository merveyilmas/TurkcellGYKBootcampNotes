-- HOMEWORK
-- SQL HomeWork

-- INNER JOIN SORULARI
-- Müşterilerin Siparişleri
-- Müşteriler (Customers) ve siparişler (Orders) tablolarını kullanarak, en az 5 sipariş vermiş müşterilerin adlarını ve verdikleri toplam sipariş sayısını listeleyin.

select * from customers
select * from orders

select c.contact_name, count(o.order_id)
from customers c
inner join orders o on c.customer_id = o.customer_id
group by c.contact_name
having count(o.order_id) > 5

-- En Çok Satış Yapan Çalışanlar
-- Çalışanlar (Employees) ve siparişler (Orders) tablolarını kullanarak, her çalışanın toplam kaç sipariş aldığını ve en çok sipariş alan 3 çalışanı listeleyin.

select * from employees
select * from orders

select e.employee_id, concat(e.first_name, ' ', e.last_name) AS full_name, count(o.order_id) as total_order
from employees e
inner join orders o on e.employee_id = o.employee_id
group by e.employee_id, e.first_name, e.last_name
order by total_order desc
limit 3

-- En Çok Satılan Ürünler
-- Sipariş detayları (Order Details) ve ürünler (Products) tablolarını kullanarak, toplamda en fazla satılan (miktar olarak) ilk 5 ürünü listeleyin.

select * from products
select * from order_details

select p.product_name, sum(od.quantity) as quantity_count
from products p
inner join order_details od on od.product_id = p.product_id
group by p.product_id
order by quantity_count desc
limit 5

-- Her Müşterinin Aldığı Kategoriler
--Müşteriler (Customers), siparişler (Orders), sipariş detayları (Order Details), ürünler (Products) ve kategoriler (Categories) tablolarını kullanarak, her müşterinin satın aldığı farklı kategorileri listeleyin.

select * from customers
select * from orders
select * from order_details
select * from products
select * from categories

select distinct c.contact_name, ct.category_name
from customers c
inner join orders o on c.customer_id = o.customer_id
inner join order_details od on o.order_id = od.order_id
inner join products p on od.product_id = p.product_id
inner join categories ct on ct.category_id = p.category_id
order by c.contact_name, ct.category_name

-- Müşteri-Sipariş-Ürün Kombinasyonu
-- Müşteriler (Customers), siparişler (Orders), sipariş detayları (Order Details) ve ürünler (Products) tablolarını kullanarak, her müşterinin kaç farklı ürün satın aldığını ve toplam kaç adet aldığını listeleyin.

select * from customers
select * from orders
select * from order_details
select * from products

select c.contact_name, count(distinct p.product_id), sum(od.quantity)
from customers c
inner join orders o on c.customer_id = o.customer_id
inner join order_details od on o.order_id = od.order_id
inner join products p on od.product_id = p.product_id
group by c.customer_id

-- LEFT JOIN SORULARI
-- Hiç Sipariş Vermeyen Müşteriler
-- Müşteriler (Customers) ve siparişler (Orders) tablolarını kullanarak, hiç sipariş vermemiş müşterileri listeleyin.

select * from customers
select * from orders

select c.contact_name
from customers c
left join orders o on c.customer_id = o.customer_id
where o.order_id is null

-- Ürün Satmayan Tedarikçiler
-- Tedarikçiler (Suppliers) ve ürünler (Products) tablolarını kullanarak, hiç ürün satmamış tedarikçileri listeleyin.

select * from suppliers
select * from products

select s.company_name
from suppliers s
left join products p on s.supplier_id = p.supplier_id
where p.product_id is null

-- Siparişleri Olmayan Çalışanlar
-- Çalışanlar (Employees) ve siparişler (Orders) tablolarını kullanarak, hiç sipariş almamış çalışanları listeleyin.

select * from employees
select * from orders

select concat(e.first_name, ' ', e.last_name) as employee_name from employees e
left join orders o on e.employee_id = o.employee_id 
where o.order_id is null

-- RIGHT JOIN SORULARI
-- Her Sipariş İçin Müşteri Bilgisi
-- RIGHT JOIN kullanarak, tüm siparişlerin yanında müşteri bilgilerini de listeleyin. Eğer müşteri bilgisi eksikse, "Bilinmeyen Müşteri" olarak gösterin.

-- coalesce(c.contact_name, 'Bilinmeyen Müşteri') --> c.contact_name null ise ona yazılan string i atar

select * from customers
select * from orders

select o.order_id, coalesce(c.contact_name, 'Bilinmeyen Müşteri') as customer_name from customers c
right join orders o on c.customer_id = o.customer_id 

-- Ürünler ve Kategorileri
-- RIGHT JOIN kullanarak, tüm kategoriler ve bu kategorilere ait ürünleri listeleyin. Eğer bir kategoriye ait ürün yoksa, kategori adını ve "Ürün Yok" bilgisini gösterin.

select * from categories
select * from products

select c.category_name, coalesce(p.product_name, 'Ürün Yok') from products p
right join categories c on p.category_id = c.category_id

-- productların hepsini getir, category'si yoksa "kategorisi yok yazsın"

select * from categories
select * from products

select p.product_name, coalesce(c.category_name, 'Kategorisi Yok') as category_name from categories c
right join products p on c.category_id = p.category_id