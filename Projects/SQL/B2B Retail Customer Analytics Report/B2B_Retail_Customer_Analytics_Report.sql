USE dqlab;

-- Data Understanding
SELECT * FROM orders_1 LIMIT 5;
SELECT * FROM orders_2 LIMIT 5;
SELECT * FROM customer LIMIT 5;

-- Total Sales and Revenue in Q1 and Q2
SELECT
    SUM(quantity) AS total_penjualan,
    SUM(quantity * priceeach) AS revenue
FROM
    orders_1
WHERE
    status = "Shipped";

SELECT
    SUM(quantity) AS total_penjualan,
    SUM(quantity * priceeach) AS revenue
FROM
    orders_2
WHERE
    status = "Shipped";

-- Percentage Growth in Total Sales and Revenue
SELECT	
	quarter,
	SUM(quantity) AS total_sales,
	SUM(quantity * priceeach) AS revenue
FROM
	(
	SELECT 
		orderNumber,
		status,
		quantity,
		priceeach,
		"1" AS quarter
	FROM 
		orders_1
	UNION
	SELECT 
		orderNumber,
		status,
		quantity,
		priceeach,
		"2" AS quarter
	FROM 
		orders_2
	 ) As tabel_a
WHERE 
	status = "Shipped"
GROUP BY
	quarter;
    
-- Is the quantity of xyz.com customers increasing?
SELECT
	quarter,
	COUNT(DISTINCT customerID) total_customers
FROM	(
	SELECT
		customerID,
		createDate,
		QUARTER(createDate) As quarter
	FROM
		customer
	) As tabel_b
WHERE 
	createDate BETWEEN "2004-01-01" AND "2004-06-30"
GROUP BY 
	quarter;
    
-- How many customers have made purchases?
SELECT
	quarter,
	COUNT(DISTINCT customerID) total_customers
FROM	
(
	SELECT
		customerID,
		createDate,
		QUARTER(createDate) As quarter
	FROM
		customer
	WHERE 
		createDate BETWEEN "2004-01-01" AND "2004-06-30"
) As table_b
WHERE
    customerID IN (
        SELECT
            DISTINCT customerID
        FROM
            orders_1
        UNION
        SELECT
            DISTINCT customerID
        FROM
            orders_2
    )
GROUP BY 
	quarter;
    
-- What are the most popular product categories among customers in Q2?
SELECT *
FROM
(
	SELECT
		categoryID,
		COUNT(DISTINCT orderNumber) As total_order,
		SUM(quantity) As total_sales
	FROM
	(
		SELECT
			productCode,
			orderNumber,
			quantity,
			status,
			SUBSTRING(productCode,1,3) AS categoryID
		FROM
			orders_2
		WHERE 
			status = "Shipped"
	) tabel_c
	GROUP BY
		categoryID
) a
ORDER BY total_order DESC;

-- How many customers remain active in transactions after their first transaction?
SELECT
	"1" AS quarter,
    COUNT(DISTINCT customerID) as total_customers
FROM
    orders_1;

SELECT
    "2" AS quarter,
    COUNT(DISTINCT customerID) AS total_customers
FROM
    orders_1
WHERE
    customerID IN(
        SELECT
            DISTINCT customerID
        FROM
            orders_2
 );