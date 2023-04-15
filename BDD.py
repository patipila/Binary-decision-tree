import pandas as pd  # biblioteka pandas służy do wczytywania danych
import math as math  # biblioteka, która wprowadza funkcje matematyczne (potrzebne do entropii)
from graphviz import Digraph  # biblioteka do tworzenia grafu binarnego drzewa decyzyjnego

# Przygotowane do wczytywania dla dowolnych danych

# file = input("Podaj ścieżkę do pliku (maiętaj o rozszerzeniu .xls").strip()  #Użytkownik ma podać ścieżkę do pliku z a pomocą funkcji input(). Wartość wprowadzona przez użytkownika zostanie przypisana do zmiennej file.
# .strip() na końcu polecenia usuwa białe znaki z początku i końca łańcucha, co może być przydatne, jeśli użytkownik przypadkowo wprowadził dodatkowe spacje przed lub po ścieżce pliku.
#sheet_name = input("Podaj nazwę arkusza w którym są dane).strip()
# premises = []
# num_premises = int(input("Podaj liczbę przesłanek: "))
# premises_len = []
# for i in range(0,num_premises):
#      premis = input("Podaj nazwę przeslanki nr " + str(i+1) + ": ")
#      attributes = int(input("Podaj liczbę atrybutów w przesłance " + str(i+1) + ": "))
#      premises.append(premis)
#      premises_len.append(attributes) #append - dodaje do listy
# num_conclusion = int(input("Podaj liczbę konluzji: "))


# Wczytanie danych z Excela jako dataframe
file = 'dane.xls'
sheet_name = 'Arkusz1'
data = pd.read_excel(file, sheet_name=sheet_name)

# Przygotowanie pod konkretne dane w projekcie
num_premises = 5  # Liczba przesłanek
premises_len = [4, 3, 3, 2, 3]  # Tablica z liczbą atrybutów dla poszczególnych przesłanek
premises = ["Ilosc wolnego miejsca ", "Budzet", "Zaangazowanie", "Uczulenie na siersc",
            "Dzieci"]  # Tablica z nazwami przeslanek
num_conclusion = 5  # Liczba mozliwych konkluzji
conclusion = "DECYZJA"  # Nazwa konkluzji

sum = num_conclusion  # do sum przypisujemy liczbę możliwych konkluzji
for i in premises_len:  # dodajemy do zmiennej sum kolumny zwierające przesłanki, aby zmienna sum przechowywała ilośc wszystkich kolumn w zbiorze danych
    sum += i

# Usuwanie niepotrzebnych kolumn powstając przy wczytaniu
columns = list(data.columns[0:sum + 1])  # data.columns tworzy listę nazw kolumn, które mają zostać zachowane w zbiorze danych.
# Argument sum+1 został dodany, aby zachować kolumny od 0 do sum włącznie, czyli sum+1 kolumn.
data = data[columns]

# drzewo decyzyjne graficznie

tree = Digraph('Jakiego psa wybrać?', filename='decisiontree.gv')
# Tworzy nowy obiekt Digraph z biblioteki graphviz, który będzie reprezentował graficzne drzewo decyzyjne
# tablica sprawdzająca czy przesłanka pojawila sie juz
repeated = []  # Tworzona jest nowa pusta lista o nazwie repeated. Ta lista będzie służyła jako tablica pomocnicza do zapisywania informacji o tym, które przesłanki zostały już wykorzystane w tworzeniu konkluzji, a które jeszcze nie.
for i in range(0, sum - num_conclusion):
    repeated.append(0)  # W każdej iteracji pętli for do listy repeated jest dodawany nowy element o wartości 0.
# W ten sposób tworzona jest lista o długości (sum-num_conclusion), która posłuży do śledzenia,
# które przesłanki zostały już wykorzystane, a które jeszcze nie.


index_conclusion = []  # Tablica pomocnicza nadająca kolejnym konkluzjom indeksy
index_conclusion.append(0)  # do listy index_conclusion dodawany jest element o wartości 0.


# Element ten jest dodawany tylko raz, poza pętlą for. Ten krok jest potrzebny do nadania indeksu pierwszej konkluzji,
# ponieważ lista index_conclusion będzie wykorzystywana w dalszej części programu do numerowania kolejnych konkluzji.

# funkcja do liczenia entropii wedlug wzoru
def entropy(ni, N):
    entropy = -(ni / N) * math.log((ni / N), 2)
    return entropy


# Funkcja wywołująca się po stwierdzeniu że potwierdzenie/zaprzeczenie warunku jednoznacznie wskazuje na jakąś konkluzję
def unique(selected_premise, selected_index, binary_result, conclusion):
    index_conclusion[0] += 1
    print("Wynik jednoznaczny: " + conclusion + " dla: " + premises[selected_premise] + ": " + columns[selected_index])
    # Graficzna reprezentacja tego, że dana przesłanka jednoznacznie wskazuje na daną konkluzję. Tworzony jest nowy wierzchołek grafu, który przedstawia daną przesłankę i jest łączony z wybraną konkluzją.
    tree.edge("(" + str(repeated[selected_index]) + ") " + premises[selected_premise] + " - " + columns[selected_index],
              "(" + str(index_conclusion[0]) + ") " + conclusion, label=binary_result)


# Główna funkcja programu - dzieląca tabelę na 2
def split(data, selected_premise, selected_index, beginning_tree, binary_result):
    print("\nSTART\n")

    data = data.reset_index(
        drop=True)  # Reset indeksu żeby przejść do kolejnego przedziału, drop=True oznacza, drop = T oznacza, ze stara wartość indeksu zostanie usunięta

    stop = 0  # warunek stopu
    N = len(data[columns[0]])  # liczba wszystkich kombinacji
    conclusion_binary_result = []  # Tablica z ni dla poszczególnych wartości konkluzji
    for i in range(sum - num_conclusion,
                   sum):  # sum - num_conclusion oznacza indeks pierwszej kolumny z wartościami konkluzyjnymi.
        temp = 0  # temp to była sum_pom
        for j in data[columns[
            i]]:  # W każdej iteracji pętli dodajemy wartości dla tej kolumny do zmiennej temp poprzez iterowanie po wartościach w kolumnie data[columns[i]].
            temp += j
        conclusion_binary_result.append(temp)  # wartości w temp są dodawane do listy conclusion_binary_result.
        if (
                temp == N):  # Jeśli wartość temp (sumowane wartości dla warunku) jest równa liczbie wszystkich kombinacji w danych (N), to oznacza to, że dany warunek gwarantuje konkluzje. W takim przypadku zmienna stop jest ustawiona na 1, a następnie wykonuje się instrukcja break, aby przerwać pętlę.
            stop = 1

            temp_2 = 0
            for x in data[columns[selected_index]]:
                temp_2 += x
            if temp_2 == 0:  # #Jeśli wartość temp_2 (suma wartości w wybranej kolumnie, która odpowiada za warunek) jest równa 0, to oznacza to, że warunek zawsze jest fałszywy, a zatem funkcja unique jest wywoływana z parametrem "nie". W przeciwnym przypadku, funkcja unique jest wywoływana z parametrem "tak"
                unique(selected_premise, selected_index, "nie", columns[i])
            else:
                unique(selected_premise, selected_index, "tak", columns[i])
            break

    if stop == 0:
        # Obliczanie Entropii dla wartości konkluzji
        I = 0
        I_j = []  # Tablica przechowujaca wartosci entropii dla różnych konkluzji
        for ni in conclusion_binary_result:
            if (ni != 0):  # Jeżeli ni jest różne od 0 wtedy liczymy entropie i dodajemy do tablicy
                E = entropy(ni, N)
                I_j.append(E)
            else:  # Jeżeli ni jest równe 0 wtedy nie wywołujemy funkcji liczącej entropii tylko do tablicy dopisujemy 0
                E = 0
                I_j.append(E)
            I += E

        # Obliczanie Entropii dla warunków
        tab_I_j_plus = []
        tab_I_j_minus = []
        tab_E_j = []
        tab_I_minus_E = []  # Tablica z której na podstawie max(I-Ej) jest wybierany warunek do dzielenia tabeli

        for j in range(0, sum - num_conclusion):
            # W każdym przebiegu pętli, algorytm oblicza wartość entropii informacji (I) dla całego zbioru danych,
            # a następnie oblicza entropie dla każdego warunku decyzyjnego (Ij+ i Ij-)
            # poprzez podział danych na dwie podgrupy - jedną zgodną z wartością warunku i drugą niezgodną z wartością warunku.
            # Następnie dla każdej wartości konkluzji, algorytm oblicza wartość entropii informacji (Xj+k) dla danej podgrupy.

            # 1) Entropia po potwierdzeniu warunku (Obliczanie Ij+)
            nj_plus = 0
            for i in data[columns[
                j]]:  # Oblicza wartość nj_plus, która jest liczbą wystąpień wartości atrybutu (j-tej kolumny w zbiorze danych) równej 1
                nj_plus += i

            tab_Xj_plus_k = []
            for k in range(0,
                           num_conclusion):  # Oblicza wartości entropii Xj+ dla każdej wartości konkluzji k po potwierdzeniu warunku j. W tym celu wykorzystuje się liczbę wystąpień wartości j=1 oraz liczby wystąpień par (j=1, konkluzja=k)
                nj_plus_k = 0
                for i in range(0, len(data[columns[j]])):
                    if (data[columns[j]][i] == 1 and data[columns[sum - num_conclusion + k]][i] == 1):
                        nj_plus_k += 1

                if (nj_plus_k == 0):
                    Xj_plus_k = 0
                else:
                    Xj_plus_k = entropy(nj_plus_k,
                                        nj_plus)  # Wywołuje funkcję entropy(nj_plus_k, nj_plus), która oblicza entropię wartości j=1 dla konkluzji k,

                tab_Xj_plus_k.append(Xj_plus_k)

            I_j_plus = 0  # Jeśli liczba wystąpień pary (j=1, konkluzja=k) jest równa zero, wartość entropii Xj_plus_k dla konkluzji k zostaje ustawiona na 0.
            for x in tab_Xj_plus_k:
                I_j_plus += x

            tab_I_j_plus.append(
                I_j_plus)  # Wartości entropii dla każdej wartości konkluzji k są dodawane do listy tab_Xj_plus_k.

            # 2) Entropia po zaprzeczeniu warunku (Obliczanie Ij-)
            nj_minus = 0
            for i in data[columns[
                j]]:  # Zliczana jest liczba takich wierszy,które są w kolumnie o indeksie j, w których wartość wynosi 0
                if (i == 0):
                    nj_minus += 1

            tab_Xj_minus_k = []
            for k in range(0,
                           num_conclusion):  # wyznaczana jest wartość liczby obiektów, dla których warunek jest niespełniony, czyli liczba obiektów, dla których wartość w kolumnie columns[j] wynosi 0
                nj_minus_k = 0
                for i in range(0, len(data[columns[j]])):
                    if (data[columns[j]][i] == 0 and data[columns[sum - num_conclusion + k]][
                        i] == 1):  # wyznaczana jest liczba obiektów, dla których warunek jest niespełniony (wartość w columns[j] jest 0) i jednocześnie wartość konkluzji wynosi k+1
                        nj_minus_k += 1

                if (nj_minus_k == 0):
                    Xj_minus_k = 0
                else:
                    Xj_minus_k = entropy(nj_minus_k, nj_minus)  # Następnie obliczana jest entropia dla tych obiektów

                tab_Xj_minus_k.append(
                    Xj_minus_k)  # Wartości entropii dla wszystkich wartości konkluzji są zapisywane do listy tab_Xj_minus_k.

            I_j_minus = 0  # Entropia po potwierdzeniu warunku j
            for x in tab_Xj_minus_k:
                I_j_minus += x

            tab_I_j_minus.append(I_j_minus)

            # Obliczenia dla Entropii po ocenie całego warunku
            # Wartość E_j, to ważona średnia wartości entropii informacji po uwzględnieniu wartości entropii Ij+ oraz Ij- dla każdej wartości konkluzji.
            E_j = (nj_plus / N) * I_j_plus + (nj_minus / N) * I_j_minus
            tab_E_j.append(E_j)
            tab_I_minus_E.append(
                I - E_j)  # obliczana jest wartość tab_I_minus_E dla każdego atrybutu j jako różnica pomiędzy całkowitą entropią (I) a E_j. Wartość ta odzwierciedla spadek entropii, który zostanie osiągnięty po wykorzystaniu atrybutu j do podziału zbioru danych. Atrybut o największej wartości tab_I_minus_E zostanie wybrany jako najlepszy atrybut.
        index = tab_I_minus_E.index(
            max(tab_I_minus_E))  # index (w tabeli) wartości przesłanki, na podstawie której będzimey dzielić tabelę

        # Przypadek w którym cała tablica I - E zawiera same 0 (Ponieważ funkcja max wybiera w tym wypadku zawsze element o indeksie 0)
        # Ten kod odpowiada za wybór kolejnego warunku do analizy w przypadku, gdy poprzednie warunki nie były wystarczająco jednoznaczne w określeniu wyniku.
        # Najpierw obliczana jest suma temp_0 wartości w tablicy tab_I_minus_E. Jeśli suma ta jest równa 0, oznacza to, że wszystkie wartości w tablicy tab_I_minus_E są równe 0. W takim przypadku następuje przeszukanie kolumn z danymi poza kolumnami zawierającymi konkluzje (tj. sum - num_conclusion kolumn) w celu znalezienia kolumny, która nie jest całkowicie pusta ani całkowicie wypełniona.
        # Jeśli takie kolumny zostanie znalezione, to jej indeks zostaje przypisany do zmiennej index, a następnie pętla jest przerywana. Jeśli jednak nie zostanie znaleziona odpowiednia kolumna, to algorytm kończy działanie.
        temp_0 = 0
        for y in tab_I_minus_E:
            temp_0 += y
        if temp_0 == 0:
            for i in range(0, sum - num_conclusion):
                temp_1 = 0
                for r in data[columns[i]]:
                    temp_1 += r
                if (temp_1 != 0 and temp_1 != len(data[columns[i]])):
                    index = i
                    break

        # Petla sprawdzajaca jaka jest nazwa przeslanki dla danego indexu
        # Przypisuje zmiennej premise_name indeks przesłanki, która odpowiada indeksowi kolumny w data, na której wykonano test jednoznaczny.
        # Zmienna premises_len zawiera informacje o liczbie kolumn dla każdej przesłanki.
        # W pętli for iterowane są wartości i z zakresu od 0 do długości listy premises_len.
        # W każdej iteracji sprawdzane jest, czy wartość index jest mniejsza niż suma dotychczasowych wartości premises_len i pom.
        # Jeśli tak, to oznacza to, że kolumna, na której wykonano test jednoznaczny, należy do przesłanki i, więc wartość premise_name jest ustawiana na i i pętla jest przerywana za pomocą instrukcji break.
        # Jeśli nie, to zmienna pom jest zwiększana o wartość premises_len[i], czyli o liczbę kolumn dla przesłanki i, aby w kolejnej iteracji pętli sprawdzić kolejną przesłankę.
        premise_name = -1
        pom = 0
        for i in range(0, len(premises_len)):
            if (index < premises_len[i] + pom):
                premise_name = i
                break
            else:
                pom += premises_len[i]

        print("Tabelę dzielimy dla przesłanki: " + premises[premise_name] + ": " + columns[
            index])  # podana jest nazwa przeslanki i indeks

        # Podział tabeli
        data1 = data[data[columns[index]] != 0]  # Tabela dla potwierdzonego warunku - wartosc 1
        data2 = data[data[columns[index]] != 1]  # Tabela dla zaprzeczonego warunku - wartosc 0
        data1 = data1.reset_index(drop=True)  # Reset indeksu
        data2 = data2.reset_index(drop=True)  # Reset indeksu

        print("Dlugosc tabeli 1: " + str(len(data1[columns[0]])))  # długość kolumny o indeksie 0 w tabeli data1
        print("Dlugosc tabeli 2: " + str(len(data2[columns[0]])))  # długość kolumny o indeksie 0 w tabeli data2

        # zaaktualizowanie tablicy przechowujacej informacje czy dana przeslanka juz sie pojawila
        repeated[index] = repeated[index] + 1

        # drzewo w formie graficznej
        if beginning_tree == 0:
            tree.edge('Jakiego psa wybrać?',
                      "(" + str(repeated[index]) + ") " + premises[premise_name] + " - " + columns[index])
        else:
            tree.edge("(" + str(repeated[selected_index]) + ") " + premises[selected_premise] + " - " + columns[
                selected_index], "(" + str(repeated[index]) + ") " + premises[premise_name] + " - " + columns[index],
                      label=binary_result)

        # instrukcje warunkowe
        # warunek pierwszy: Jeśli długość kolumny o indeksie 0 z tabel, to wykonaj pustą instrukcję (pass).
        # Oznacza to, że w przypadku gdy obie tabele zawierają tylko po jednym wierszu, nie zostanie wykonana żadna akcja.

        # warunek drugi: Jeśli długość kolumny o indeksie 0 z tabel wynosi 0, to wykonaj pass.
        # Oznacza to, że w przypadku gdy obie tabele zawierają tylko po jednym wierszu, nie zostanie wykonana żadna akcja.

        # warunek trzeci:
        # Jeśli jednak długość kolumny o indeksie 0 w danych data1 i data2 nie jest ani równa 1, ani 0, to wywoływana jest funkcja split

        if len(data1[columns[0]]) == 1 and len(data2[columns[0]]) == 1:
            pass
        elif (len(data1[columns[0]]) == 0 or len(data2[columns[0]]) == 0):
            pass
        else:
            split(data1, premise_name, index, 1, "tak")
            split(data2, premise_name, index, 1, "nie")


split(data, 0, 0, 0, "nie")  # uzywamy funkcji split
print(tree.source)  # drzewo w formie tekstowej
tree.view()  # rysowanie drzewa w formie graficznej
