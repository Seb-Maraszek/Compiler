Kompilator napisany jest w języku Python, korzystając z biblioteki PLY.


Instalacja potrzebnych bibliotek:
	sudo apt install python3
	sudo apt install python3-pip
	pip3 install ply
	
Uruchomienie:
	python3 compiler.py <plik wejściowy> <plik wyjściowy>
	
Program testowany był na pythonie 3.8.5 i taką wersję zalecam (ze starszymi może być problem ze względu na użycie różnych dość świeżych funkcji)

Zawartość:
	W folderze helpers znajdują się pliki 'generator' oraz 'program' które bezpośrednio 	odpowiadają za generowanie wyjściowyego ciągu rozkazów maszyny.
 	
 

