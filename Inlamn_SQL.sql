-- Betyg G Queries
    -- För att visa kunskaper på G-nivå skall du redovisa SQL-satser som ger svar på följande 
    -- sju frågor kring data i databasen SverigeData.db.
    -- Tänk på utdata från dina redovisade SQL-satser endast innehålla för frågan 
    -- relevanta data.

    -- 1. Vad är länsbokstaven för Blekingelän?

    SELECT bokstav, namn
    FROM lan
    WHERE namn like "blekinge lan"

    -- 2. Vad är folkmängden för Skånelän?

    SELECT namn, folkmangd
    FROM lan
    WHERE namn like "skane lan"

    -- 3. Vilka tätorter har namn som slutar på stad?

    SELECT namn
    FROM Tatorter
    WHERE namn like "%stad"

    -- 4. Vilka tätorter har 249 invånare?

    SELECT namn, folkmangd
    FROM Tatorter
    WHERE folkmangd like "249"

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

    SELECT namn, folkmangd
    FROM Lan
    ORDER BY folkmangd ASC

    --7. Vilka tätorter i Västerbottens län har mer än 1000 invånare och ligger i kommuner som har mindre än 4000 invånare?
    
    SELECT tat.kod as 'Tatort Kod',
    tat.namn as Tatort,
    tat.folkmangd as 'Tatord Folk',
    kom.namn as Kommun,
    kom.folkmangd as 'Kommun Folk',
    Lan.namn as Lan
    FROM Tatorter tat
    JOIN Kommuner kom ON tat.kommun=kom.kod
    JOIN Lan ON kom.lan=Lan.kod
    WHERE Lan.namn LIKE "vasterbottens lan" AND tat.folkmangd > 1000 AND
    kom.folkmangd < 4000
--

-- Betyg VG Queries
    -- För att visa kunskaper på VG-nivå skall du, utöver det som krävs för G-nivå 
    -- och utan att använda SQL-vyer, redovisa SQL-satser som ger svar på följande 
    -- fem frågor kring data i databasen SverigeData.db.

    -- 1. Vad heter residensstaden i Blekinge län? -Dubbel kolla-
    
    SELECT kod, namn
    FROM Tatorter
    WHERE kod Like (SELECT Lan.residensstad
    FROM Lan
    WHERE Lan.namn LIKE "Blekinge lan")

    SELECT Lan.namn, Lan.residensstad, Tatorter.namn
    FROM Lan
    JOIN Tatorter ON Lan.residensstad=Tatorter.kod
    WHERE Lan.namn='Blekinge lan'
    
    -- 2. Finns det någon kommun utan tätorter? Vilken i så fall? - W.I.P-
    
    SELECT kod, namn, kommun
    FROM Tatorter
    WHERE kommun ISNULL

    
    -- 3. Vad heter Sveriges minsta kommun (till folkmängd räknat)
    
    SELECT namn, MIN(folkmangd)
    FROM Kommuner
    
    -- 4. Vad heter den nordligaste tätorten i landet? (Använd latituden för tätorter!)
    
    SELECT namn, MAX(latitud)
    from Tatorter
    
    -- 5. Hur många bor det i residensstaden i Värmlands län
    
    SELECT Lan.namn, Lan.residensstad, Tatorter.namn, Tatorter.folkmangd
    FROM Lan
    JOIN Tatorter ON Lan.residensstad = Tatorter.kod
    WHERE Lan.namn LIKE "varmlands lan"

    SELECT *
    FROM Lan
    WHERE namn='Varmlands lan'
