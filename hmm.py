from read_midi import *
from hmmlearn.hmm import MultinomialHMM
import numpy as np
np.set_printoptions(suppress=True)
input_file = '/Users/liuxinhong/Documents/毕业论文/数据集/rap beat/scrub_A#_144bpm_dripchord.midi'
Midi = MyMidi(input_file)
data = np.array(Midi.read_midi(ins = 'Keys', show_hist = False)).reshape(-1,1)

#train hmm
model = MultinomialHMM(n_components = 10)
model.fit(data)
print(model.emissionprob_)

#generate
sample = model.sample(120)
sample = sample[0].flatten().tolist()
Midi.convert_to_midi(sample, input_file.rsplit('/', 1)[0] + '/hmm.midi')