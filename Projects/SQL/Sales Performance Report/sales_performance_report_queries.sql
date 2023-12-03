USE dqlab;

-- 1. Overall Performance by Year
SELECT
    YEAR(order_date) AS years,
    SUM(sales) AS sales,
    COUNT(order_id) AS number_of_order
FROM
    dqlab_sales_store
WHERE
    order_status = 'Order Finished'
GROUP BY
    years
ORDER BY
    years ASC;
    
-- 2. Overall Performance by Product Sub-Category
SELECT 
	YEAR(order_date) AS years,
	product_sub_category,
	SUM(sales) AS sales
FROM 
	dqlab_sales_store
WHERE
	YEAR(order_date) IN (2011,2012)
    AND order_status = 'Order Finished'
GROUP BY 
	years,
	product_sub_category
ORDER BY 
	years, sales desc;
    
-- 3. Promotion Effectiveness and Efficiency by Years
SELECT
    YEAR(order_date) AS years,
    SUM(sales) AS sales,
	SUM(discount_value) AS promotion_value,
	ROUND((SUM(discount_value)/SUM(sales))*100, 2) As burn_rate_percentage
FROM
    dqlab_sales_store
WHERE
    order_status = 'Order Finished'
GROUP BY
    years
ORDER BY
    years ASC;

-- 4. Promotion Effectiveness and Efficiency by Product Sub Category
SELECT
    YEAR(order_date) AS years,
	product_sub_category,
	product_category,
    SUM(sales) AS sales,
	SUM(discount_value) AS promotion_value,
	ROUND((SUM(discount_value)/SUM(sales))*100, 2) As burn_rate_percentage
FROM
    dqlab_sales_store
WHERE
	YEAR(order_date) = '2012'
	AND order_status = 'Order Finished'
GROUP BY
    years,
	product_sub_category,
	product_category
ORDER BY
    sales DESC;
    
-- 5. New Customers Each Year
SELECT
    YEAR(order_date) AS years,
    COUNT(DISTINCT customer) AS number_of_customer
FROM
    dqlab_sales_store
WHERE
    order_status = 'order finished'
GROUP BY
    years
ORDER BY
    years ASC;

	
    

