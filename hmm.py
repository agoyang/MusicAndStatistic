from read_midi import *
from hmmlearn.hmm import MultinomialHMM
import numpy as np
np.set_printoptions(suppress=True)
input_file = '/Users/liuxinhong/Documents/毕业论文/数据集/twinkle/35393.midi'
Midi = MyMidi(input_file)
data, chord_data = Midi.read_notes(ins = 'Piano', show_hist = False)
Midi.remember_chord(isForgeting=False)
data = np.array(data).reshape(-1,1)
chord_data = np.array(chord_data).reshape(-1,1)

#train hmm
model = MultinomialHMM(n_components = 3)
model.fit(data)
chord_model = MultinomialHMM(n_components = 3)
chord_model.fit(chord_data)

#generate
sample = model.sample(120)
sample = sample[0].flatten().tolist()
chord_sample = chord_model.sample(40)
chord_sample = chord_sample[0].flatten().tolist()
Midi.convert_to_midi(sample, chord_sample, input_file.rsplit('/', 1)[0] + '/hmm.midi', isUsingLearnt=True)