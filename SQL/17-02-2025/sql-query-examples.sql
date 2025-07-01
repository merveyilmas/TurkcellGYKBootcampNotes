-- 1️⃣ En Çok Satış Yapan Çalışanı Bulun
-- Her çalışanın (Employees) sattığı toplam ürün adedini hesaplayarak, en çok satış yapan ilk 3 çalışanı listeleyen bir sorgu yazınız.
-- İpucu: Orders, OrderDetails ve Employees tablolarını kullanarak GROUP BY ve ORDER BY yapısını oluşturun. TOP 3 veya LIMIT ile ilk 3 çalışanı seçin.

select * from employees
select * from orders
select * from order_details

select concat(e.first_name, ' ', e.last_name), count(od.product_id * od.quantity) as total_product from employees e
inner join orders o on e.employee_id = o.employee_id
inner join order_details od on o.order_id = od.order_id
group by e.employee_id
order by total_product desc
limit 3


-- 2️⃣ Aylık Satış Trendlerini Bulun
-- Siparişlerin (Orders) hangi yıl ve ayda ne kadar toplam satış geliri oluşturduğunu hesaplayan ve yıllara göre sıralayan bir sorgu yazınız.
-- İpucu: Orders ve OrderDetails tablolarını kullanın. Tarih bilgisini yıl ve aya göre gruplayın, toplam satış gelirini hesaplayarak sıralayın.

--- EXTRACT(YEAR FROM ...) - yıl bilgisi
--- EXTRACT(MONTH FROM ...) - ay bilgisi

select * from orders 
select * from order_details

select o.order_id, extract(year from o.order_date) as order_year, extract(month from o.order_date) as order_month,
sum(od.unit_price * od.quantity) as total_price
from orders o
inner join order_details od on o.order_id = od.order_id
group by o.order_id, order_year, order_month
order by order_year, order_month


-- 3️⃣ En Karlı Ürün Kategorisini Bulun
-- Her ürün kategorisinin (Categories), o kategoriye ait ürünlerden (Products) yapılan satışlar sonucunda elde ettiği toplam geliri hesaplayan bir sorgu yazınız.
-- İpucu: Categories, Products, OrderDetails ve Orders tablolarını birleştirin. Kategori bazında gelir hesaplaması yaparak en yüksekten en düşüğe sıralayın.

select * from categories  
select * from products
select * from orders  
select * from order_details

select c.category_name, sum(od.unit_price * quantity) as total_price
from categories c 
inner join products p on c.category_id = p.category_id
inner join order_details od on p.product_id = od.product_id
inner join orders o on od.order_id = o.order_id
group by c.category_name
order by total_price desc


-- 4️⃣ Belli Bir Tarih Aralığında En Çok Sipariş Veren Müşterileri Bulun
-- 1997 yılında en fazla sipariş veren ilk 5 müşteriyi listeleyen bir sorgu yazınız.
-- İpucu: Orders ve Customers tablolarını birleştirin. WHERE ile 1997 yılını filtreleyin, müşteri bazında sipariş sayılarını hesaplayarak sıralayın ve en fazla sipariş veren 5 müşteriyi seçin.

select * from orders  
select * from customers  

select c.contact_name, extract(year from o.order_date) as order_year, 
count(o.order_id) as total_order_count
from customers c
inner join orders o on c.customer_id = o.customer_id
group by c.contact_name, extract(year from o.order_date)
having extract(year from o.order_date) = 1997
order by total_order_count desc
limit 5

-- 5️⃣ Ülkelere Göre Toplam Sipariş ve Ortalama Sipariş Tutarını Bulun
-- Müşterilerin bulunduğu ülkeye göre toplam sipariş sayısını ve ortalama sipariş tutarını hesaplayan bir sorgu yazınız. Sonucu toplam sipariş sayısına göre büyükten küçüğe sıralayın.
-- İpucu: Customers, Orders ve OrderDetails tablolarını birleştirin. Ülke bazında GROUP BY kullanarak toplam sipariş sayısını ve ortalama sipariş tutarını hesaplayın.
 
select * from customers 
select * from orders 
select * from order_details

select c.country, count(o.order_id) as total_order_count, avg(od.unit_price * od.quantity) as avg_order_amount
from customers c
inner join orders o on c.customer_id = o.customer_id
inner join order_details od on o.order_id = od.order_id
group by c.country
order by total_order_count desc