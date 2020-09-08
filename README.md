# Robot Localization
1. Funkcja odpowiadająca za model sensora oraz przejścia:
W celu obliczenia prawdopodobieństwa lokacji oraz orientacji, w jakiej znajduje się agent wykorzystane zostały 3 macierze:
- 'arr_loc' - zawiera prawdopodobieństwo z jakim agent znajduje się w każdej lokacji
- 'arr_sensor' - zawiera wartość zgodności z odczytem z sensora dla każdej lokacji oraz orientacji agenta 
- 'arr_orient' - zawiera prawdopodobieństwo orientacji agenta

    W pętli głównej sprawdzane jest, jaką poprzednią akcję wykonał agent oraz co wykazały sensory i na tej podstawie wyliczane są oraz uzupełniane wcześniej wspomniane macierze. Jeśli poprzednią akcją było 'forward', możemy uzupełnić macierz orientacji wartościami 1 na głównej przekątnej, ponieważ na pewno nie zmieniła się nasza orientacja. Dodatkowo, jesli 'percept' zwróciło wartość 'bump' mamy 100% pewność, że robot nie zmienił swojej lokacji. W przypadku, gdy poprzednią akcją był skręt w dowolnym kierunku, również możemy uzupełnić macierz lokacji wartościami 1 na głównej przekątnej. W dalszej części sprawdzane są odczyty z sensorów. W końcowej fazie wszystkie macierze 'składane' są w jedną.


2. Funkcja odpowiadająca za heurystykę agenta jest dość prosta:  

- jeśli jest możliwość (sensor nie wykrywa przeszkody), robot skręca w lewo po czym kieruje się przed siebie
- jeśli nie ma opcji skrętu w lewo, agent kieruje się na wprost
- jeśli nie ma możliwości skrętu w lewo lub pójścia prosto, agent ostatecznie pójdzie w prawo

    W kodzie zostały dodane zabezpieczenia, aby robot nie kręcił się w kółko w jednym polu (sprawdzanie, czy ostatnim ruchem był skręt), lub żeby nie zapętlił się w czterach sąsiadujących polach (gdy tak się stanie, priorytetem jest pójście w prawo).
