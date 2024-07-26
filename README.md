AIDEV23S_UW - Webbportfölj inlämning

- GitHub Link: https://github.com/Lindayh/AIDEV23S_UW_Inlamn01.git

"Projektet är en personlig webbportfölj med olika sektioner: about me, contact me, skills, GitHub-portfölj och referenser. Det går också att ladda ner CV:n. Man navigerar till olika sektioner genom att välja den relativa fliken, ingen scrollning behövs.
    
Semantiken är bara en enkel navbar, footer och hero/main. Varje sektion har en olika layout för att ge lite variation.

JS:
Tabs: de skapades med JS som styr display css elementet, så bara den valda article visas medan alla andra döljs. 
Jag testade också pure-CSS tabs men det var lättare att ha bättre semantics med JS. Pure-CSS krävde tabs innehåll som child till radio-knappar som sitter i navbar.
Contact me form: information kontrolleras när man klickar utanför input element (out of focus). Email kontrolleras också när man skriver i fältet. 
Om vissa information är fel då visas ett meddelande bredvid den relativa input field. Tomma fält betraktas som ogiltiga.
”Send” knappen gör en kontroll till och en alert meddelar om allt gick bra eller om informationen behöver rättas. 
Weather API: openweather API anropas direkt för Stockholm. Information för att få rätt vädersikon finns redan i datan från API:n, den behöver bara kombineras med resten av URL:en.

Responsivitet: Webbportföljen skapades desktop-first, med en tablet- och en mobilversion. I de två versionerna finns det ingen hero, bara en navbar med menyn och en header som funkar som home knapp.