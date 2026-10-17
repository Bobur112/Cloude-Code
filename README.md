# Pelengator — mobil pelengator apparati dasturiy ta'minoti

Innotexnopark loyihasi. Ko'p kanalli (faza-kogerent) SDR va antenna massivi orqali radio
signal manbasining kelish yo'nalishini (DoA, azimut) aniqlaydi.

## Hozirgi holat (v0.1)
- Antenna geometriyasi: doiraviy (UCA) va chiziqli (ULA) massivlar
- Algoritmlar: Bartlett va MUSIC (ko'p manbali)
- Simulyator va testlar (SDR apparati hali ulanmagan)

## Ishga tushirish
```bash
pip install -e ".[dev]"
pytest
pelengator --freq 433e6 --azimuth 42 200 --method music
```

## Keyingi qadamlar
SDR drayveri (KrakenSDR/RTL-SDR), kanallarni kalibrovka qilish, GPS va xarita, real vaqtli interfeys, jurnalga yozish.
