import os
import csv
import shutil
import argparse

csv_files = [
    {
        'file': 'campaign/abilities.csv',
        'key_columns': ['id'],
        'translation_columns': ['name', 'desc']
    },
    {
        'file': 'campaign/commodities.csv',
        'key_columns': ['id'],
        'translation_columns': ['name', 'desc']
    },
    {
        'file': 'campaign/industries.csv',
        'key_columns': ['id'],
        'translation_columns': ['name', 'desc']
    },
    {
        'file': 'campaign/market_conditions.csv',
        'key_columns': ['id'],
        'translation_columns': ['name', 'desc']
    },
    {
        'file': 'campaign/reports.csv',
        'key_columns': ['event_type', 'event_stage', 'channels', 'target_rel'],
        'translation_columns': ['subject', 'summary', 'assessment']
    },
    {
        'file': 'campaign/special_items.csv',
        'key_columns': ['id'],
        'translation_columns': ['name', 'desc']
    },
    {
        'file': 'campaign/special_items.csv',
        'key_columns': ['id'],
        'translation_columns': ['name', 'desc']
    },
    {
        'file': 'campaign/submarkets.csv',
        'key_columns': ['id'],
        'translation_columns': ['name', 'desc']
    },
    {
        'file': 'strings/descriptions.csv',
        'key_columns': ['id'],
        'translation_columns': ['text1']
    }
]

local_directory = 'data'
translation_directory = 'translations'

source_directory = 'C:\\Program Files (x86)\\Fractal Softworks\\Starsector\\starsector-core\\data'
# source_directory = '/home/grena/Documents/data'

def fetch_new_translations(file_info):
    source_file = os.path.join(source_directory, file_info['file'])
    local_file = os.path.join(local_directory, file_info['file'])
    translation_file = os.path.join(translation_directory, file_info['file'])

    # Copier le fichier source dans le répertoire local
    os.makedirs(os.path.dirname(local_file), exist_ok=True)
    shutil.copyfile(source_file, local_file)

    # Créer le répertoire de traduction s'il n'existe pas
    os.makedirs(translation_directory, exist_ok=True)
    os.makedirs(os.path.dirname(translation_file), exist_ok=True)

    # Vérifier si le fichier source existe
    if os.path.exists(source_file):
        # Lire le fichier de traduction et retenir les id déjà existant
        seen_rows = set()
        mode = 'w' # Mode d'écriture du fichier de traduction

        if os.path.exists(translation_file):
            mode = 'a' # On passe en mode ajout si le fichier existe déjà
            with open(translation_file, 'r', encoding='utf-8') as fs_translation_file:
                translation_csv = csv.DictReader(fs_translation_file)
                for row in translation_csv:
                    key = tuple(row[key_column] for key_column in file_info['key_columns'])
                    seen_rows.add(key)

        # Lire le fichier source et copier les colonnes spécifiées dans le fichier de traduction
        with open(source_file, 'r', encoding='utf-8') as source_file, \
             open(translation_file, mode, newline='', encoding='utf-8') as translation_file:
            source_csv = csv.DictReader(source_file)
            columns_to_copy = file_info['key_columns'] + file_info['translation_columns']
            translation_csv = csv.DictWriter(translation_file, fieldnames=columns_to_copy, quotechar='"', quoting=csv.QUOTE_ALL)

            # Écrire l'entête si le fichier est nouveau
            if mode == 'w':
                translation_csv.writeheader()

            for row in source_csv:
                # Construire la clé en fonction des colonnes discriminantes
                key = tuple(row[key_column] for key_column in file_info['key_columns'])

                # Vérifier si la clé n'a pas déjà été vue pour éviter les doublons
                if key not in seen_rows:
                    seen_rows.add(key)
                    translation_csv.writerow({col: row[col] for col in columns_to_copy})

        print(f"Traitement de '{source_file.name}' et écriture dans '{translation_file.name}'")
    else:
        print(f"Le fichier '{source_file.name}' n'a pas été trouvé.")

def write_new_translations(file_info):
    translation_file = os.path.join(translation_directory, file_info['file'])
    local_file = os.path.join(local_directory, file_info['file'])

    # Vérifier si le fichier de traduction existe
    if os.path.exists(translation_file) and os.path.exists(local_file):
        # Charger les traductions existantes dans un dictionnaire en utilisant l'ID comme clé
        existing_translations = {}
        with open(translation_file, 'r', encoding='utf-8') as tf:
            translation_csv = csv.DictReader(tf)
            for row in translation_csv:
                key = tuple(row[key_column] for key_column in file_info['key_columns'])
                existing_translations[key] = row

        # Lire le fichier local pour mettre à jour les data
        updated_data = []
        with open(local_file, 'r', encoding='utf-8') as lf:
            local_csv = csv.DictReader(lf)
            for row in local_csv:
                key = tuple(row[key_column] for key_column in file_info['key_columns'])

                # Vérifier si l'ID existe dans les traductions existantes
                if key in existing_translations:
                    # Mettre à jour les valeurs des colonnes spécifiées
                    existing_translation = existing_translations[key]
                    for col in file_info['translation_columns']:
                        row[col] = existing_translation[col]

                # Ajouter la ligne mise à jour à la liste des traductions
                updated_data.append(row)

        # Écrire les traductions mises à jour dans le fichier local
        with open(local_file, 'w', newline='', encoding='utf-8') as lf:
            local_csv = csv.DictWriter(lf, fieldnames=updated_data[0].keys(), quotechar='"', quoting=csv.QUOTE_MINIMAL)
            local_csv.writeheader()
            for data in updated_data:
                local_csv.writerow(data)

        print(f"Traductions mises à jour pour '{file_info['file']}'")
    else:
        print(f"Le fichier '{translation_file}' ou '{local_file}' n'existe pas.")

def main():
    parser = argparse.ArgumentParser(description='Copier et traiter des fichiers .csv pour la traduction de Starsector.')
    parser.add_argument('--action', choices=['fetch', 'write'], required=True, help='Action à effectuer: fetch pour récupérer les nouveaux fichiers du jeu, write pour écrire les traductions dans le mod')

    args = parser.parse_args()

    if args.action == 'fetch':
        for file_info in csv_files:
            fetch_new_translations(file_info)

    elif args.action == 'write':
        for file_info in csv_files:
            write_new_translations(file_info)

if __name__ == "__main__":
    main()
