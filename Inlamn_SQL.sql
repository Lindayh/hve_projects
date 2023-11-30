-- 1. Vad är länsbokstaven för Blekingelän?

SELECT bokstav
FROM Lan
WHERE namn LIKE "blekinge lan"

-- 2. Vad är folkmängden för Skånelän?

SELECT folkmangd
FROM lan
WHERE namn LIKE "skane lan"

-- 3. Vilka tätorter har namn som slutar på stad?

SELECT namn
FROM Tatorter
WHERE namn LIKE "%stad"

-- 4. Vilka tätorter har 249 invånare?

SELECT namn
FROM Tatorter
WHERE folkmangd LIKE "249"

-- 5. Vad heter länet som tätorten Mariedal ligger i?

SELECT Lan.namn
FROM Lan
WHERE Lan.kod LIKE (
SELECT Kommuner.lan
FROM Kommuner WHERE
Kommuner.kod LIKE
(SELECT Tatorter.kommun
FROM Tatorter
WHERE Tatorter.namn LIKE "Mariedal"))

-- 6. Lista alla län i storleksordning i avseende på befolkningen, med minst befolkningen överst.

SELECT namn
FROM Lan
ORDER BY folkmangd ASC

--7. Vilka tätorter i Västerbottens län har mer än 1000 invånare och ligger i kommuner som har mindre än 4000 invånare?

SELECT tat.namn
FROM Tatorter tat
JOIN Kommuner kom ON tat.kommun=kom.kod
JOIN Lan ON kom.lan=Lan.kod
WHERE Lan.namn LIKE "vasterbottens lan" AND tat.folkmangd > 1000 AND
kom.folkmangd < 4000

-- 1. Vad heter residensstaden i Blekinge län? 

SELECT namn
FROM Tatorter
WHERE kod LIKE (SELECT Lan.residensstad
FROM Lan
WHERE Lan.namn LIKE "Blekinge lan"

SELECT Lan.namn
FROM Lan
JOIN Tatorter ON Lan.residensstad=Tatorter.kod
WHERE Lan.namn = 'Blekinge lan'

-- 2. Finns det någon kommun utan tätorter? Vilken i så fall?

SELECT kommun
FROM Tatorter
WHERE kommun ISNULL

-- 3. Vad heter Sveriges minsta kommun (till folkmängd räknat)

SELECT namn, MIN(folkmangd)
FROM Kommuner

SELECT namn
FROM Kommuner
ORDER BY folkmangd ASC
LIMIT 1

-- 4. Vad heter den nordligaste tätorten i landet? (Använd latituden för tätorter!)

SELECT namn, MAX(latitud)
from Tatorter

SELECT namn
FROM Tatorter
ORDER BY latitud DESC
LIMIT 1

-- 5. Hur många bor det i residensstaden i Värmlands län

SELECT 
Tatorter.folkmangd
FROM Lan
JOIN Tatorter ON Lan.residensstad = Tatorter.kod
WHERE Lan.namn LIKE "varmlands lan"
