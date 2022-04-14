from music21 import *
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import random
import pickle

class MyMidi():
    def __init__(self, file):
        self.file = file
        self.show_instrument()
        self.learnt_chord = []

    def show_instrument(self):
        #parsing a midi file
        midi = converter.parse(self.file)
    
        #grouping based on different instruments
        s2 = instrument.partitionByInstrument(midi)

        for part in s2.parts:
            print(str(part))

    def read_notes(self, ins, threshold = 0, show_hist = True):

        #ins(str): selected instrument
        file = self.file
        print("Loading Music File:",file)
        
        notes = []
        chord_list = []
        chord_dur = []
        dur = []
        chord_pitch = {}
        notes_to_parse = None
        
        #parsing a midi file
        midi = converter.parse(file)
    
        #grouping based on different instruments
        s2 = instrument.partitionByInstrument(midi)

        #Looping over all the instruments
        for part in s2.parts:
            
            if ins in str(part): 
                print("selected instrument:",str(part))
                notes_to_parse = part.recurse() 
        
                for element in notes_to_parse:
                    
                    #note
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                        dur.append(element.duration.quarterLength)
                    
                    #chord
                    elif isinstance(element, chord.Chord):

                        if random.random() > 0.95:
                            self.learnt_chord.append(element)

                        for p in element.pitches:
                            chord_pitch[str(p)] = 0
                        chord_list.append('.'.join(str(n) for n in element.normalOrder))
                        chord_dur.append(element.duration.quarterLength)
                        # notes.append('.'.join(str(n) for n in element.normalOrder))
                        # dur.append(element.duration.quarterLength)

                    #rest
                    # elif isinstance(element, note.Rest):
                    #     notes.append(element.name)
                    #     dur.append(element.duration.quarterLength)

                    elif isinstance(element, tempo.MetronomeMark):
                        self.tempo = element

        self.chord_pitch = chord_pitch
        notes = np.array(notes)
        df = pd.DataFrame()
        df['notes'] = notes
        # df.loc[df['notes'].isin(chord_pitch.keys()), 'notes'] = 'rest'  #notes that appear in chord_pitch are replace with rest
        df['duration'] = dur
        self.note_dur = dur
        # print(df[df['notes'] != 'rest'])
        freq = dict(Counter(notes))
        no=[count for _,count in freq.items()]
        plt.figure(figsize=(5,5))
        plt.hist(no[1:])
        plt.title('Hist without the most frequent')
        if show_hist:   plt.show()
        frequent_notes = [note for note, count in freq.items() if count>=threshold]
        
        df = df[df['notes'].isin(frequent_notes)]
        int_seq, self.unique = pd.factorize(list(zip(df.notes, df.duration)))
        # int_seq, self.unique = pd.factorize(df.notes)

        int_chord, self.chord_code = pd.factorize(chord_list)
        
        self.chord_dur = list(set(chord_dur))

        return int_seq, int_chord

    def remember_chord(self, isForgeting = False):
        mode = 'ab'
        if isForgeting: mode = 'wb'
        with open('learnt_chord.pickle', mode) as f:
            pickle.dump(self.learnt_chord, f)

    def recall_chord(self):
        with open('learnt_chord.pickle', "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break


    def convert_to_midi(self, predictions, chord_int, fname, isUsingLearnt=True):
        if isUsingLearnt:
            chord_generator = self.recall_chord()
        prediction_output = [self.unique[i] for i in predictions]
        chord_output = [self.chord_code[i] for i in chord_int]

        offset = 0
        output_notes = []
        for pattern in chord_output:
            notes_in_chord = pattern.split('.')
            notes = []
            dur = random.choice(self.chord_dur)
            for current_note in notes_in_chord:
                
                cn=int(current_note)
                new_note = note.Note(cn)
                new_note.duration.quarterLength = dur
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)  
                
            new_chord = chord.Chord(notes)
            if isUsingLearnt and random.random() > 0.8:
                try:
                    chord_pickle = next(chord_generator)
                except:
                    chord_pickle = []
                if chord_pickle:
                    new_chord = random.choice(chord_pickle)
                    for p in new_chord:
                        self.chord_pitch[str(p)] = 0
            new_chord.offset = offset
            output_notes.append(new_chord)
            offset += dur

        offset = 0
        
        #use tempo from train data if possible
        if self.tempo is not None:
            output_notes.append(self.tempo)

        # create note and chord objects based on the values generated by the model
        for pattern in prediction_output:
            dur = pattern[1]
            # dur = random.choice(self.note_dur)
            pattern = pattern[0]

            #patten is a rest
            if pattern == 'rest':
                new_rest = note.Rest()
                new_rest.duration.quarterLength = dur
                new_rest.offset = offset
                output_notes.append(new_rest)
                
            # pattern is a note
            else:
                
                new_note = note.Note(pattern)
                new_note.storedInstrument = instrument.Piano()
                if str(pattern) in self.chord_pitch:
                    new_note = note.Rest()
                new_note.duration.quarterLength = dur
                new_note.offset = offset
                output_notes.append(new_note)

            offset += dur

        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp=fname)