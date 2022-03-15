from read_midi import *
from hmmlearn.hmm import MultinomialHMM
import numpy as np
np.set_printoptions(suppress=True)
Midi = MyMidi('/Users/liuxinhong/Documents/毕业论文/数据集/rap beat/Fit_The_Description_C#_162_dripchord.mid')
data = np.array(Midi.read_midi(ins = '', show_hist = True, threshold = 3)).reshape(-1,1)
model = MultinomialHMM(n_components = 5)
model.fit(data)
print(model.emissionprob_)
sample = model.sample(120)
sample = sample[0].flatten().tolist()
Midi.convert_to_midi(sample, '/Users/liuxinhong/Documents/毕业论文/数据集/rap beat/hmmv2_Fit_The_Description_C#_162_dripchord.mid')