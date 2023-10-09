## Starsector - French Translation mod
Mod de traduction FR pour le jeu [Starsector](https://fractalsoftworks.com/).

## Installation

- [Téléchargez le mod au format .zip](https://github.com/grena/starsector_french_translation_mod/archive/refs/heads/main.zip)
- Extraire le .zip et le mettre dans le dossier "mods" de Starsector, situé dans `C:\Program Files (x86)\Fractal Softworks\Starsector\mods`
- Au lancement du jeu, activer le mod "French Translation"

## Participer à la traduction

Tous les fichiers dans le dossier `data` du mod sont **générés**, il ne faut donc **pas y toucher directement**.

Les fichiers à traduire sont dans le dossier `translations`.

Pour générer les fichiers `data`, il faut lancer le script python :
```sh
python3 fetch_new_strings.py --action write
```

## Récupérer les chaines après un patch du jeu

Quand une nouvelle version du jeu sort, il faut récupérer les nouvelles chaines à traduire :
```sh
python3 fetch_new_strings.py --action fetch

# puis réécrire les traductions

python3 fetch_new_strings.py --action write
```

## About
Initiated [in 2017 by Neuroxer](https://fractalsoftworks.com/forum/index.php?topic=12799.msg216851#msg216851) then abandoned, I've decided to revive this translation project and move it to GitHub to ease collaboration and maintenance.
