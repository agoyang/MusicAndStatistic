cd /Users/liuxinhong/Documents/thesis/google-research
virtualenv fad
source fad/bin/activate
python -m pip install --upgrade pip
pip install apache-beam numpy scipy tensorflow
touch tensorflow_models/__init__.py
touch tensorflow_models/audioset/__init__.py
python -m frechet_audio_distance.gen_test_files --test_files "test_audio"
ls --color=never test_audio/background/*  > test_audio/test_files_background.cvs
ls --color=never test_audio/test1/*  > test_audio/test_files_test1.cvs
ls --color=never test_audio/test2/*  > test_audio/test_files_test2.cvs
python -m frechet_audio_distance.create_embeddings_main --input_files test_audio/test_files_background.cvs --stats stats/background_stats
python -m frechet_audio_distance.create_embeddings_main --input_files test_audio/test_files_test1.cvs --stats stats/test1_stats
python -m frechet_audio_distance.create_embeddings_main --input_files test_audio/test_files_test2.cvs --stats stats/test2_stats
python -m frechet_audio_distance.compute_fad --background_stats stats/background_stats --test_stats stats/background_stats