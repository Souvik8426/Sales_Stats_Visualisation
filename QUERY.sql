CREATE DATABASE ELECTRONICS;
	USE ELECTRONICS;
	SELECT * FROM PRODUCT ORDER BY CAST(SUBSTRING(P_ID, 2,LEN(P_ID) - 1 ) AS INT);
	SELECT * FROM PURCHASE ORDER BY CAST(SUBSTRING(P_ID, 2,LEN(P_ID) - 1 ) AS INT);
	SELECT * FROM USERS ORDER BY CAST(SUBSTRING(USER_ID, 2,LEN(USER_ID) - 1 ) AS INT);




---Q1: NUMBER OF PURCHASES ACC TO YEARS---
SELECT YEAR, COUNT(*) AS Purchase_Count
FROM PURCHASE
GROUP BY YEAR ORDER BY YEAR;


---Q2: NUMBER OF PURCHASES BASED ON THE BRAND---
SELECT BRAND, COUNT(*) AS Purchase_Count
FROM PRODUCT
GROUP BY BRAND;

---Q3: NUMBER OF PURCHASES BASED ON THE ITEM_ID---
SELECT ITEM_ID, COUNT(*) AS Purchase_Count
FROM PRODUCT
GROUP BY ITEM_ID
ORDER BY Purchase_Count DESC;

---Q4: NUMBER OF PURCHASES OF MALE AND FEMALE---
SELECT USER_ATTR, COUNT(*) AS Purchase_Count
FROM USERS
GROUP BY USER_ATTR;


---Q5: NO OF PRODUCTS WITH DIFFERENT RATINGS---
SELECT RATING, COUNT(*) AS Purchase_Count
FROM PRODUCT
GROUP BY RATING ORDER BY RATING;
-----------------------------------------------
---Q6: NO OF PURCHASES BASED ON MODEL ATTRIBUTE---
SELECT MODEL_ATTR, COUNT(*) AS Purchase_Count
FROM PRODUCT
GROUP BY MODEL_ATTR
ORDER BY Purchase_Count DESC;

----------------------------------------------
--- Q7: NUMBER OF PURCHASES BASED ON ITEM_ID---
SELECT ITEM_ID, COUNT(*) AS Purchase_Count
FROM PRODUCT
GROUP BY ITEM_ID;

----------------------------------------------
--- Q8: NUMBER OF PURCHASES MADE IN EACH MONTH BASED ON PARTICULAR YEAR---
SELECT YEAR, MONTH, COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 1999 
GROUP BY YEAR, MONTH ORDER BY MONTH;

SELECT YEAR, MONTH, COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2000
GROUP BY YEAR, MONTH ORDER BY MONTH;

SELECT YEAR, MONTH, COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2001  
GROUP BY YEAR, MONTH ORDER BY MONTH;

SELECT YEAR, MONTH, COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2002 
GROUP BY YEAR, MONTH ORDER BY MONTH;

SELECT YEAR, MONTH, COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2003  
GROUP BY YEAR, MONTH ORDER BY MONTH;

SELECT YEAR, MONTH, COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2004
GROUP BY YEAR, MONTH ORDER BY MONTH;

SELECT YEAR, MONTH, COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2005 
GROUP BY YEAR, MONTH ORDER BY MONTH;

SELECT YEAR, MONTH, COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2006 
GROUP BY YEAR, MONTH ORDER BY MONTH;

---------------------------------------------
---Q9: AVGERAGE RATING BASED ON BRAND---
SELECT BRAND, AVG(RATING) AS Avg_Rating
FROM PRODUCT
GROUP BY BRAND;

--- Q10: Identify the top 3 brands with the highest average rating---
SELECT *
FROM (
    SELECT BRAND, AVG(RATING) AS Avg_Rating,
           ROW_NUMBER() OVER (ORDER BY AVG(RATING) DESC) AS rank
    FROM PRODUCT
    GROUP BY BRAND
) AS ranked
WHERE rank <= 3;


------------------------------------------------------------
---Q11: IDENTIFYING THE SALES PER YEAR IN QUARTERS 
SELECT YEAR, 
       CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 1999
GROUP BY YEAR, 
         CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
         END;

SELECT YEAR, 
       CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2000
GROUP BY YEAR, 
         CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
         END;

SELECT YEAR, 
       CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2001
GROUP BY YEAR, 
         CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
         END;

SELECT YEAR, 
       CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2002
GROUP BY YEAR, 
         CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
         END;

SELECT YEAR, 
       CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2003
GROUP BY YEAR, 
         CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
         END;

SELECT YEAR, 
       CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2004
GROUP BY YEAR, 
         CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
         END;

SELECT YEAR, 
       CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2005
GROUP BY YEAR, 
         CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
         END;

SELECT YEAR, 
       CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
       END AS Quarter,
       COUNT(*) AS Purchase_Count
FROM PURCHASE
WHERE YEAR = 2006
GROUP BY YEAR, 
         CASE
           WHEN MONTH IN (1, 2, 3) THEN 'Q1'
           WHEN MONTH IN (4, 5, 6) THEN 'Q2'
           WHEN MONTH IN (7, 8, 9) THEN 'Q3'
           ELSE 'Q4'
         END;

------------------------------------------------