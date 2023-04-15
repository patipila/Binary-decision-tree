# Drzewo decyzyjne 

#  Teoria
Drzewo decyzyjne to graficzna reprezentacja decyzji podejmowanych w oparciu o zestaw reguł. Algorytm ID3 to jedna z metod budowy drzew decyzyjnych, która opiera się na wyborze atrybutów o największym znaczeniu w podejmowaniu decyzji. W tym algorytmie, entropia jest miarą nieokreśloności lub nieporządku danych, która jest wykorzystywana do obliczenia informacyjnej wartości każdego atrybutu. Im mniejsza entropia, tym większa informacyjna wartość atrybutu. W procesie tworzenia drzewa decyzyjnego, algorytm ID3 iteracyjnie wybiera atrybut o największej informacyjnej wartości i tworzy węzeł drzewa na podstawie tego atrybutu.


# Opis programu
Program generujący drzewo decyzyjne dla problemu wyboru filmu został napisany w języku Python 3.10, w środowisku PyCharm Community Edition 2022.2.2. Drzewo zostało ostatecznie wygenerowane z pomocą zewnętrznego programu Graphviz. Dzięki programowi możliwe jest wygenerowanie drzewa dla dowolnych danych z pliku  xls. 

# Wymagane biblioteki
	import pandas as pd 
	import math as math  
	from graphviz import Digraph  
	import os
Biblioteka `math` nie wymaga instalacji.
Aby zainstalować bibliotekę `pandas` w terminalu należy wpisać komendę:

	pip install pandas

Dla komputerów o systemie macOS należy w terminalu wpisać komendę :
 
	/bin/bash -c "$(curl-fsSLhttps://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Następnie w terminalu należy wpisać:

	brew install grapviz

Dla komputerów o systemie Windows należy w terminalu wpisać komendę :
```
winget install graphviz
```

# Przygotowanie danych 
Program pobiera dane z tabeli w Excelu, w której przesłanki oraz konkluzje uporządkowane są poziomo i przypisane są im wartości 0 lub 1. Ważne, aby plik z danymi miał rozszerzenie .xls

W pliku znajduje się również kod, który może służyć do wczytania przez użytkownika dowolnego zestawu danych. Do sprawdzenia naszego zestawu został on zakomentowany. 

# Najważniejsze funkcje 
- Entropy

		entropy(ni, N)
	Funkcja obliczająca entropię.
- Unique

		unique(selected_premise, selected_index, binary_result, conclusion)

Funkcja, która stosowana jest w momencie, gdy dla potwierdzenia lub zaprzeczenia danego warunku występuje jednoznaczna konkluzja.
- Split

		split(data, selected_premise, selected_index, beginning_tree, binary_result):

Funkcja, która na podstawie miar zysku informacyjnego zapisywanych do wektora, wybiera wartość maksymalną i dzieli tabelę na dwie na podstawie przesłanki, dla której wartość ta jest największa. Wyjątkiem jest przypadek, gdy wartości zysku informacyjnego dla każdej przesłanki są równe 0 – wtedy wybierana jest pierwsza wartość w tablicy, dla której wartości nie są identyczne (to znaczy nie występują same 0 ani same 1).


# Działanie programu
Po każdej iteracji program zwraca wynik, który pokazuje w jaki sposób podzielono tabelę lub, która przesłanka została wybrana jako jednoznaczna.

