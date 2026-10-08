# Suami Pergi ke Pasar — animasi kartun 9:16

Video jadi: `output/suami_pergi_ke_pasar.mp4` (720x1280, 30 fps).

## Ganti suara pakai ElevenLabs
Taruh MP3 dari ElevenLabs di folder `voices/`, satu file per baris dialog:

| File | Pembicara | Dialog |
|---|---|---|
| 01.mp3 | SUAMI | Aku pergi dulu, ya. |
| 02.mp3 | ISTRI | Mau ke mana? |
| 03.mp3 | SUAMI | Ke pasar. |
| 04.mp3 | ISTRI | Aku ikut. |
| 05.mp3 | SUAMI | Ngapain kamu ikut segala? |
| 06.mp3 | ISTRI | Please. |
| 07.mp3 | SUAMI | Ya udah, oke. |
| 08.mp3 | ISTRI | Tunggu dua menit ya, aku pakai sandal dulu. |
| 09.mp3 | SUAMI | Oke. |
| 10.mp3 | ISTRI | Ayo. |
| 11.mp3 | ISTRI | Tuh kan, pergi duluan, dasar anjing! Awas aja nanti kalau pulang, aku kasih 'makan' yang enak. |
| 12.mp3 | ISTRI | Nunggu dua menit aja nggak bisa. |
| 13.mp3 | SUAMI | Ada apa nih? |
| 14.mp3 | ISTRI | Ayo, baby. |
| 15.mp3 | ANAK | (tertawa) Wah, mantap! |

File yang tidak ada akan memakai TTS lokal (espeak-ng + MBROLA). Timing animasi & gerak mulut otomatis mengikuti durasi audio.

## Build
```bash
B=build; mkdir -p $B
python3 src/voices.py . $B
NODE_PATH=$(npm root -g) node src/render.js src/scene.html $B/timeline.json $B/frames
ffmpeg -framerate 30 -i $B/frames/%05d.png -i $B/voice.wav -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest output/suami_pergi_ke_pasar.mp4
```
Butuh: python3, ffmpeg, espeak-ng + mbrola-id1, node + playwright.
