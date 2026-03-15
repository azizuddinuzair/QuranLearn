---
dataset_info:
  features:
  - name: surah_id
    dtype: int32
  - name: ayah_id
    dtype: int32
  - name: word_id
    dtype: string
  - name: word_index
    dtype: int32
  - name: word_ar
    dtype: string
  - name: word_en
    dtype: string
  - name: word_tr
    dtype: string
  - name: surah_name_ar
    dtype: string
  - name: surah_name_en
    dtype: string
  - name: ayah_ar
    dtype: string
  - name: audio
    dtype: audio
  splits:
  - name: train
    num_bytes: 2164094570
    num_examples: 77429
  download_size: 2049220107
  dataset_size: 2164094570
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
# Quran-MD - Word Level

This dataset is part of the complete Quran-MD dataset available here: **[Complete Quran-MD](https://huggingface.co/datasets/Buraaq/quran-audio-text-dataset)**

### Paper
**Quran-MD: A Fine-Grained Multimodal Dataset of the Quran** 
(Accepted at: 5th Muslims in ML Workshop co-located with NeurIPS 2025)

📄 **Paper Link:** [quran-md-paper](https://arxiv.org/abs/2601.17880)
### Abstract

> We present Quran-MD, a comprehensive multimodal dataset of the Qur’an that integrates textual, linguistic, and audio dimensions at the verse and word levels. For each verse (ayah), the dataset provides its original Arabic text, English translation, and phonetic transliteration. To capture the rich oral tradition of Qur’anic recitation, we include verse-level audio from 30 distinct reciters, reflecting diverse recitation styles and dialectical nuances. At the word level, each token is paired with its corresponding Arabic script, English translation, transliteration, and an aligned audio recording, allowing fine-grained analysis of pronunciation, phonology, and semantic context. This dataset supports various applications, including natural language processing, speech recognition, text-to-speech synthesis, linguistic analysis, and digital Islamic studies. Bridging text and audio modalities across multiple reciters, this dataset provides a unique resource to advance computational approaches to Qur’anic recitation and study. Beyond enabling tasks such as ASR, tajweed detection, and Qur’anic TTS, it lays the foundation for multimodal embeddings, semantic retrieval, style transfer, and personalized tutoring systems that can support both research and community applications.


## Dataset Description

This dataset contains **77,429 individual word-level audio recordings** from the complete Quran with precise pronunciations. Each sample includes a single word pronunciation along with its Arabic text, English meaning, transliteration, and contextual information from the source verse.


### Dataset Summary

- **📝 Audio Samples**: 77,429 MP3 files (individual word pronunciations)
- **📚 Coverage**: Complete Quran vocabulary (114 surahs)
- **🌐 Languages**: Arabic (original), English (meanings), Transliteration
- **🎧 Audio Quality**: High-quality word-level segmentation
- **⏱️ Duration**: Approximately ~20 hours of word-level audio
- **🔍 Granularity**: Individual word pronunciation with position context
- **Morphological Diversity**: Various grammatical forms and inflections


### Supported Tasks

- **🔤 Pronunciation Training**: Learn individual Arabic word pronunciation
- **📊 Linguistic Analysis**: Study Quranic vocabulary and morphology
- **🎯 Word Spotting**: Train word detection models
- **📖 Vocabulary Building**: Arabic language learning
- **🔍 Audio Segmentation**: Word-level audio alignment research
- **🎙️ Fine-grained ASR**: Word-level Arabic speech recognition


### Languages

- **Arabic** (Classical Arabic - Quranic Arabic)
- **English** (translations)
- **Transliteration** (romanized Arabic)


## Dataset Structure

Each sample contains individual word information with contextual metadata:

```python
{
    "surah_id": int32,           # Source surah (chapter) number
    "ayah_id": int32,            # Source ayah (verse) number  
    "word_id": string,           # Unique word identifier
    "word_index": int32,         # Position of word within the ayah (0-based)
    "word_ar": string,           # Individual word in Arabic
    "word_en": string,           # Word meaning/translation in English
    "word_tr": string,           # Word transliteration (romanized)
    "surah_name_ar": string,     # Context: Source surah name in Arabic
    "surah_name_en": string,     # Context: Source surah name in English
    "ayah_ar": string,           # Context: Complete ayah text for reference
    "audio": Audio(),            # Audio file (MP3 format) - isolated word
}
```

### Sample Data Example

```python
{
    "surah_id": 1,
    "ayah_id": 1,
    "word_id": "1:1:1",
    "word_index": 0,
    "word_ar": "بِسْمِ",
    "word_en": "In the name",
    "word_tr": "Bismi", 
    "surah_name_ar": "الفاتحة",
    "surah_name_en": "Al-Fatiha",
    "ayah_ar": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
    "audio": <Audio object>  # Isolated pronunciation of "بِسْمِ"
}
```


## Usage Examples

### Loading the Dataset

```python
from datasets import load_dataset

# Load the Word-level dataset  
dataset = load_dataset("Buraaq/quran-md-words")

print(f"Dataset size: {len(dataset):,} word recordings")
print(f"Sample keys: {list(dataset[0].keys())}")

# Access first sample
first_word = dataset[0]
print(f"Word: {first_word['word_ar']} ({first_word['word_tr']})")
print(f"Meaning: {first_word['word_en']}")
print(f"Context: {first_word['ayah_ar']}")
print(f"Position: Word {first_word['word_index'] + 1} in Surah {first_word['surah_id']}, Ayah {first_word['ayah_id']}")
```

### Play Word Audio

```python
import IPython.display as ipd

# Play individual word pronunciation
first_word = dataset[0]
print(f"Playing pronunciation of: {first_word['word_ar']} ({first_word['word_tr']})")
ipd.Audio(first_word["audio"]["array"], rate=first_word["audio"]["sampling_rate"])
```

### Vocabulary Analysis

```python
# Find all instances of a specific word
target_word = "اللَّهِ"  # "Allah"
allah_instances = dataset.filter(lambda x: x["word_ar"] == target_word)
print(f"Word '{target_word}' appears {len(allah_instances):,} times")

# Show contexts where this word appears
for i in range(min(5, len(allah_instances))):
    instance = allah_instances[i]
    print(f"Surah {instance['surah_id']}, Ayah {instance['ayah_id']}: {instance['ayah_ar']}")
```

### Word Length Analysis

```python
# Analyze word lengths
word_lengths = [len(sample["word_ar"]) for sample in dataset.select(range(1000))]
print(f"Average word length: {sum(word_lengths)/len(word_lengths):.2f} characters")
print(f"Shortest word: {min(word_lengths)} characters")  
print(f"Longest word: {max(word_lengths)} characters")

# Find shortest and longest words
shortest_words = dataset.filter(lambda x: len(x["word_ar"]) == min(word_lengths))
longest_words = dataset.filter(lambda x: len(x["word_ar"]) == max(word_lengths))

print(f"\\nShortest words examples:")
for i in range(min(3, len(shortest_words))):
    word = shortest_words[i]
    print(f"  {word['word_ar']} ({word['word_tr']}) - {word['word_en']}")
```

### Build Vocabulary Dictionary

```python
# Create vocabulary with meanings
vocabulary = {}
unique_words = set()

for sample in dataset.select(range(10000)):  # Sample for performance
    word_ar = sample["word_ar"]
    if word_ar not in vocabulary:
        vocabulary[word_ar] = {
            "transliteration": sample["word_tr"],
            "meanings": [sample["word_en"]],
            "count": 1,
            "contexts": [sample["ayah_ar"]]
        }
        unique_words.add(word_ar)
    else:
        vocabulary[word_ar]["count"] += 1
        if sample["word_en"] not in vocabulary[word_ar]["meanings"]:
            vocabulary[word_ar]["meanings"].append(sample["word_en"])

print(f"Unique words found: {len(unique_words):,}")
print(f"Most frequent words:")

# Sort by frequency
sorted_vocab = sorted(vocabulary.items(), key=lambda x: x[1]["count"], reverse=True)
for word, data in sorted_vocab[:10]:
    print(f"  {word} ({data['transliteration']}): {data['count']} times - {', '.join(data['meanings'])}")
```

### Filter by Word Position

```python
# Find all words that start verses (position 0)
verse_starters = dataset.filter(lambda x: x["word_index"] == 0)
print(f"Words that start verses: {len(verse_starters):,}")

# Find common verse-starting words
starter_words = {}
for sample in verse_starters.select(range(1000)):
    word = sample["word_ar"]
    starter_words[word] = starter_words.get(word, 0) + 1

print("Most common verse-starting words:")
for word, count in sorted(starter_words.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {word}: {count} verses")
```

### Extract Words from Specific Ayah

```python
# Get all words from Al-Fatiha, first ayah
al_fatiha_words = dataset.filter(lambda x: x["surah_id"] == 1 and x["ayah_id"] == 1)
print(f"Al-Fatiha first ayah has {len(al_fatiha_words)} words")

# Display words in order
words_ordered = sorted(al_fatiha_words, key=lambda x: x["word_index"])
ayah_reconstruction = []

for word in words_ordered:
    print(f"Word {word['word_index'] + 1}: {word['word_ar']} ({word['word_tr']}) - {word['word_en']}")
    ayah_reconstruction.append(word['word_ar'])

print(f"\\nReconstructed ayah: {' '.join(ayah_reconstruction)}")
print(f"Original ayah: {words_ordered[0]['ayah_ar']}")
```


## Advanced Usage

### Building Pronunciation Models

```python
# Extract features for pronunciation modeling
import librosa
import numpy as np

def extract_word_features(audio_array, sample_rate):
    # Extract MFCC features
    mfccs = librosa.feature.mfcc(y=audio_array, sr=sample_rate, n_mfcc=13)
    # Extract spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=audio_array, sr=sample_rate)
    return {
        'mfccs': mfccs.mean(axis=1),
        'spectral_centroid': spectral_centroids.mean()
    }

# Process sample words
features_data = []
for i in range(100):  # Sample processing
    sample = dataset[i]
    audio = sample["audio"]["array"]
    sr = sample["audio"]["sampling_rate"]
    features = extract_word_features(audio, sr)
    features_data.append({
        'word': sample["word_ar"],
        'features': features
    })
```

### Word Similarity Analysis

```python
# Find similar sounding words
from difflib import SequenceMatcher

def find_similar_words(target_word, dataset_sample, threshold=0.6):
    similar_words = []
    target_tr = None
    
    # Find target word's transliteration
    for sample in dataset_sample:
        if sample["word_ar"] == target_word:
            target_tr = sample["word_tr"]
            break
    
    if not target_tr:
        return similar_words
    
    # Find similar transliterations
    for sample in dataset_sample:
        similarity = SequenceMatcher(None, target_tr.lower(), sample["word_tr"].lower()).ratio()
        if similarity > threshold and sample["word_ar"] != target_word:
            similar_words.append({
                'word': sample["word_ar"],
                'transliteration': sample["word_tr"],
                'meaning': sample["word_en"],
                'similarity': similarity
            })
    
    return sorted(similar_words, key=lambda x: x['similarity'], reverse=True)

# Example usage
similar = find_similar_words("اللَّهِ", dataset.select(range(1000)))
print("Words similar to 'اللَّهِ':")
for word_info in similar[:5]:
    print(f"  {word_info['word']} ({word_info['transliteration']}) - {word_info['similarity']:.2f}")
```

## Citation

```bibtex
@misc{salman2026quranmdfinegrainedmultilingualmultimodal,
      title={Quran-MD: A Fine-Grained Multilingual Multimodal Dataset of the Quran}, 
      author={Muhammad Umar Salman and Mohammad Areeb Qazi and Mohammed Talha Alam},
      year={2026},
      eprint={2601.17880},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2601.17880}, 
}
```

## Related Datasets

- **📝 [Quran-MD - Ayah](https://huggingface.co/datasets/Buraaq/quran-md-ayahs)**: Complete verse recitations (187,080 samples)
- **🏠 [Complete Quran-MD Overview](https://huggingface.co/datasets/Buraaq/quran-audio-text-dataset)**: Full dataset collection documentation

## Contact

- **Hugging Face Profile**: umarsalman
- **GitHub Profile**: umar1997
- **Dataset Issues**: Please open an issue on the repository.

Feel free to reach out for dataset issues, research collaborations, or community contributions.

---

*"And We have certainly made the Quran easy for remembrance, so is there any who will remember?"* - Quran 54:17