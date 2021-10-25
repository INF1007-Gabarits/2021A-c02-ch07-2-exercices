#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mido


notes_per_octave = 12


def build_note_dictionaries(note_names, add_octave_no=True):
	c0_midi_no = 12 # Plus basse note sur les pianos est La 0, mais on va commencer à générer les noms sur Do 0

	midi_to_name = {}
	name_to_midi = {}
	# Pour chaque octave de 0 à 8 (inclus). On va générer tout l'octave 8, même si la dernière note du piano est Do 8
	for octave in range(8+1):
		# Pour chaque note de l'octave
		for note in range(notes_per_octave):
			# Calculer le numéro MIDI de la note et ajouter aux deux dictionnaires
			midi_no = c0_midi_no + octave * notes_per_octave + note
			# Ajouter le numéro de l'octave au nom de la note si add_octave_no est vrai
			full_note_name = note_names[note] + (str(octave) if add_octave_no else "")
			midi_to_name[midi_no] = full_note_name
			# Garder les numéros de notes dans name_to_midi entre 0 et 11 si add_octave_no est faux
			name_to_midi[full_note_name] = midi_no if add_octave_no else midi_no % notes_per_octave
	return midi_to_name, name_to_midi

def build_print_note_name_callback(midi_to_name):
	pass

def build_print_chord_name_callback(chord_names_and_notes, name_to_midi):
	# Construire le dictionnaire d'assocations entre état des notes et accord joué.
	# Par exemple, [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0] -> "Do majeur"
	chords = {}
	# Pour chaque nom d'accord (clé) et notes de l'accord (valeur) :
	for name, notes in chord_names_and_notes.items():
		# On construit d'abord un liste à False qui va contenir l'état des notes associé à l'accord
		chord_notes = [False] * notes_per_octave
		# Pour chaque note de l'accord
		for note in notes:
			# On convertit le nom de la note en son numéro MIDI à l'aide du dictionnaire `name_to_midi`,
			# puis on utilise ce numéro (entre 0 et 11) comme index dans la liste.
			chord_notes[name_to_midi[note] % notes_per_octave] = True
		# On ne peut pas utiliser une liste comme clé de dictionnaire, donc on convertit en tuple.
		chords[tuple(chord_notes)] = name

	# Créez et retourner le callback
	pass

# Variable globale qui contient l'état des notes de l'octave (1 = appuyée, 0 = relâchée)
note_states = [False] * 12


def main():
	# Affiche les ports MIDI que mido reconnait.
	available_input_ports = mido.get_input_names()
	print(f"Liste des ports MIDI disponibles : {available_input_ports}")

	# Des ports MIDI affichés précédement, choisissez celui qui vous convient.
	port_midi = "3- UM-ONE 0"

	english_names = ["C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
	solfeggio_names = ["Do", "Réb", "Ré", "Mib", "Mi", "Fa", "Fa#", "Sol", "Lab", "La", "Sib", "Si"]

	midi_to_name_eng_8va, name_to_midi_eng_8va = build_note_dictionaries(english_names, True)
	midi_to_name_fr, name_to_midi_fr = build_note_dictionaries(solfeggio_names, False)
	print(midi_to_name_eng_8va[64])
	print(name_to_midi_eng_8va["C0"])
	print(midi_to_name_fr[61])
	print(midi_to_name_fr[73])
	print(name_to_midi_fr["Fa#"])

	input("Appuyez sur ENTER pour passer à l'étape suivante...")
	print("- - " * 30)

	midi_to_name, name_to_midi = build_note_dictionaries(solfeggio_names, True)
	print_note_name = build_print_note_name_callback(midi_to_name)
	keyboard = mido.open_input(port_midi, callback=print_note_name)

	input("Affichage des noms de notes (Appuyez sur ENTER pour passer à l'étape suivante)..." "\n")
	keyboard.close()

	print("- - " * 30)

	chord_names = {
		"Do majeur" : ("Do", "Mi", "Sol"),
		"Fa majeur" : ("Fa", "La", "Do"),
		"Sol majeur" : ("Sol", "Si", "Ré"),
		"La mineur" : ("La", "Do", "Mi")
	}
	
	midi_to_name, name_to_midi = build_note_dictionaries(solfeggio_names, False)
	print_chord_name = build_print_chord_name_callback(chord_names, name_to_midi)
	keyboard = mido.open_input(port_midi, callback=print_chord_name)
	
	input("Affichage des noms d'accords (Appuyez sur ENTER pour passer à l'étape suivante)..." "\n")
	keyboard.close()

if __name__ == "__main__":
	main()
