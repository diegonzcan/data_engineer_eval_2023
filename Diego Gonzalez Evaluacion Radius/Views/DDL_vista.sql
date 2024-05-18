## PARTICIPACION PRODUCTO Y TERRITORIO POR MES Y AÑO

##VARIABLES: AÑO, #MES, #TERRITORIO, #PRODUCTO, #VENTAS
CREATE OR REPLACE VIEW Participaciones AS (
WITH BASE AS (  # Base con suma de las ventas agrupadas al nivel de granularidad
	SELECT  YEAR(y.OrderDate) AÑO,
			MONTH(y.OrderDate) MES,
			z.Name AREA,	
			x.ProductID ID_PRODUCTO,
			ROUND(SUM(x.OrderQTY * x.LineTotal),2) INGRESOS
		FROM sales.salesorderdetail x
	LEFT JOIN sales.salesorderheader y 
		ON x.SalesOrderID = y.SalesOrderID
	LEFT JOIN sales.salesterritory z 
		ON y.TerritoryID = z.TerritoryID
	GROUP BY 1,2,3,4	)
SELECT 	DISTINCT  # Se calcula la participacion como la suma al nivel mas bajo dividido por el totalizador
		AÑO, MES, AREA, ID_PRODUCTO,
		INGRESOS/SUM(INGRESOS) OVER (PARTITION BY AÑO, MES) 'Participacion en Absoluta del Periodo',
        INGRESOS/SUM(INGRESOS) OVER (PARTITION BY AÑO, MES, AREA) 'Participacion en Area',
        INGRESOS/SUM(INGRESOS) OVER (PARTITION BY AÑO, MES, ID_PRODUCTO) 'Participacion en Producto'
FROM BASE 
ORDER BY 1,2,3,4 )


