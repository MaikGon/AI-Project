# Robot Localization
Funkcja odpowiadająca za heurystykę agenta jest dość prosta:  

- jeśli jest możliwość (sensor nie wykrywa przeszkody), robot skręca w lewo po czym kieruje się przed siebie

- jeśli nie ma opcji skrętu w lewo, agent kieruje się na wprost

- jeśli nie ma możliwości skrętu w lewo lub pójścia prosto, agent ostatecznie pójdzie w prawo

W kodzie zostały dodane zabezpieczenia, aby robot nie kręcił się w kółko w jednym polu (sprawdzanie, czy ostatnim ruchem był skręt), lub żeby nie zapętlił się w czterach sąsiadujących polach (gdy tak się stanie, priorytetem jest pójście w prawo).
