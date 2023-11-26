-- SALES ANALYSIS IN A STORE
-- 1. Total amount of all sales (total/revenue)
SELECT
    SUM(total) AS total
FROM
    tr_penjualan;

-- 2. Total quantity of all sold products
SELECT
    SUM(qty) AS qty
FROM
    tr_penjualan;

-- 3. Total quantity and total revenue for each product code
SELECT
    kode_produk,
    SUM(qty) AS qty,
    SUM(total) AS total
FROM
    tr_penjualan
GROUP BY
    kode_produk;

-- 4. Average total spending per customer code
SELECT
    kode_pelanggan,
    AVG(total) AS avg_total
FROM
    tr_penjualan
GROUP BY
    kode_pelanggan;

/* 5. Added a new column with the name 'category' which categorizes total/revenue into 3 categories: High: > 300K; Medium: 100K - 300K; Low: <100K. */
SELECT
    kode_transaksi,
    kode_pelanggan,
    no_urut,
    kode_produk,
    nama_produk,
    qty,
    total,
    CASE
        WHEN total > 300000 THEN 'High'
        WHEN total < 100000 THEN 'Low'
        ELSE 'Medium'
    END AS kategori
FROM
    tr_penjualan;
