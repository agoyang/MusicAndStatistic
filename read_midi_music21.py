from music21 import *
import os
import numpy as np


def read_midi(file, ins):
    #ins(str): selected instrument
    
    print("Loading Music File:",file)
    
    notes=[]
    notes_to_parse = None
    
    #parsing a midi file
    midi = converter.parse(file)
  
    #grouping based on different instruments
    s2 = instrument.partitionByInstrument(midi)

    #Looping over all the instruments
    for part in s2.parts:
        print("selected instrument:",str(part))
        if ins in str(part): 
        
            notes_to_parse = part.recurse() 
      
            #finding whether a particular element is note or a chord
            for element in notes_to_parse:
                
                #note
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                
                #chord
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))

    return np.array(notes)

file = '/Users/liuxinhong/Documents/毕业论文/数据集/35393.midi'

#reading each midi file
notes = read_midi(file, 'Piano')

unique_x = list(set(notes.ravel()))
x_note_to_int = dict((notes, number) for number, notes in enumerate(unique_x))

x_seq=[]
for i in notes:
    #assigning unique integer to every note
    x_seq.append(x_note_to_int[i])

print(x_seq)
    
