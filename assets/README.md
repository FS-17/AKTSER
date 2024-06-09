# AKTSER Test Assets

This directory contains audio files used for developing and testing AKTSER, the Telegram bot that summarizes voice messages.

## Files

### Original Test Audio
- [test0.wav](assets/test0_cut.wav)
- [test1.wav](assets/test1_cut.wav)
- [test2.ogg](assets/test2_cut.ogg)

These files were sourced from YouTube videos to simulate real-world voice messages with varying lengths, speech patterns, and background noise.

### Processed Audio
- [test0_cut.wav](assets/test0_cut.wav)
- [test1_cut.wav](assets/test1_cut.wav)
- [test2_cut.wav](assets/test2_cut.wav)

These are the outputs of AKTSER's audio trimming feature, which removes silence and low-volume segments from the original files. They demonstrate how AKTSER can reduce message length without losing content.

## Audio Sources

thank to creators of the following videos for providing diverse audio content that helped shape AKTSER's capabilities:

1. **test0.wav**:
   - Duration: 18s
   - Description: a AI generated voice message.
   - Trimming Result: 11s (39% reduction)

2. **test1.wav**: [Youtube](https://www.youtube.com/watch?v=uZRCisaS-bY&ab_channel=TravellerMovement)
   - Duration: 48s
   - Description: random english talk.
   - Trimming Result: 44s (8% reduction)

3. **test2.wav**: [Youtube](https://www.youtube.com/watch?v=sqv44Msl6rg&ab_channel=%D8%A5%D8%B0%D8%A7%D8%B9%D8%A9%D8%AB%D9%85%D8%A7%D9%86%D9%8A%D8%A9)
   - Duration: 57s
   - Description: arabic talk.
   - Trimming Result: 51s (11% reduction)

## Usage in Development

1. **Algorithm Testing**: Used to fine-tune our silence detection and trimming algorithms.
2. **Accuracy Verification**: Manually verified that trimmed files retain all important content.
3. **Edge Cases**: Helped identify challenges like distinguishing between intentional pauses and unnecessary silence.

## Legal Note

These audio files are used under Fair Use for educational and research purposes. If you're a content owner and have concerns, please [contact me](https://t.me/FAS17px)

## Related Jupyter Notebook

For detailed analysis of these audio files, including waveform visualization and statistical analysis, see [`../analyze.ipynb`](../analyze.ipynb).

---

AKTSER: Summarizing voices, saving time. 🎙️⏱️