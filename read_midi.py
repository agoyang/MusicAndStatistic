from hashlib import new
from music21 import *
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

class MyMidi():
    def __init__(self, file):
        self.file = file
        self.show_instrument()

    def show_instrument(self):
        notes=[]
        notes_to_parse = None
        #parsing a midi file
        midi = converter.parse(self.file)
    
        #grouping based on different instruments
        s2 = instrument.partitionByInstrument(midi)

        for part in s2.parts:
            print(str(part))

    def read_midi(self, ins, threshold = 3, show_hist = True):

        #ins(str): selected instrument
        file = self.file
        print("Loading Music File:",file)
        
        notes = []
        dur = []
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
        
                for element in notes_to_parse:
                    
                    #note
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                        dur.append(element.duration.quarterLength)
                    
                    #chord
                    elif isinstance(element, chord.Chord):
                        notes.append('.'.join(str(n) for n in element.normalOrder))
                        dur.append(element.duration.quarterLength)
                    elif isinstance(element, note.Rest):
                        notes.append(element.name)
                        dur.append(element.duration.quarterLength)
        notes = np.array(notes)
        df = pd.DataFrame()
        df['notes'] = notes
        df['duration'] = dur
        freq = dict(Counter(notes))
        no=[count for _,count in freq.items()]
        plt.figure(figsize=(5,5))
        plt.hist(no[1:])
        plt.title('Hist without the most frequent')
        if show_hist:   plt.show()
        frequent_notes = [note for note, count in freq.items() if count>=threshold]
        
        df = df[df['notes'].isin(frequent_notes)]
        int_seq, self.unique = pd.factorize(list(zip(df.notes, df.duration)))
        return int_seq

    def convert_to_midi(self, predictions, fname, skip_rest_rate = 0.3):
        prediction_output = [self.unique[i] for i in predictions]
        offset = 0
        output_notes = []

        # create note and chord objects based on the values generated by the model
        for pattern in prediction_output:
            dur = pattern[1]
            pattern = pattern[0]
            # pattern is a chord
            if ('.' in pattern) or pattern.isdigit():
                notes_in_chord = pattern.split('.')
                notes = []
                for current_note in notes_in_chord:
                    
                    cn=int(current_note)
                    new_note = note.Note(cn)
                    new_note.duration.quarterLength = dur
                    new_note.storedInstrument = instrument.Piano()
                    notes.append(new_note)  
                    
                new_chord = chord.Chord(notes)
                new_chord.offset = offset
                output_notes.append(new_chord)

            #patten is a rest
            elif pattern == 'rest':
                new_rest = note.Rest()
                new_rest.duration.quarterLength = dur
                new_rest.offset = offset
                output_notes.append(new_rest)
                
            # pattern is a note
            else:
                
                new_note = note.Note(pattern)
                new_note.duration.quarterLength = dur
                new_note.offset = offset
                new_note.storedInstrument = instrument.Piano()
                output_notes.append(new_note)

            if dur > 1:
                offset += 1
            else:
                offset += dur
        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp=fname)