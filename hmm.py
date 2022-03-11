from read_midi import *
from hmmlearn.hmm import MultinomialHMM
Midi = MyMidi('/Users/liuxinhong/Documents/毕业论文/数据集/35393.midi')
data = np.array(Midi.read_midi('Piano')).reshape(-1, 1)
model = MultinomialHMM(n_components = 4)
model.fit(data)
sample = model.sample(60)
sample = sample[0].flatten().tolist()
Midi.convert_to_midi(sample, '/Users/liuxinhong/Documents/毕业论文/数据集/hmm.midi')