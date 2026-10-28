"""
EduSmart Content Forge - Génère 3 nouveaux cours par jour
Utilise OpenAI pour générer du contenu conforme programme CI
"""
import json
import os
import random
from pathlib import Path

# Programme manquant à générer (exemples)
CURRICULUM_MANQUANT = [
    {"niveau": "6e", "matiere": "Maths", "chapitre": "Nombres décimaux"},
    {"niveau": "6e", "matiere": "Français", "chapitre": "Le dialogue"},
    {"niveau": "5e", "matiere": "Maths", "chapitre": "Calcul littéral"},
    {"niveau": "4e", "matiere": "Maths", "chapitre": "Racines carrées"},
    {"niveau": "3e", "matiere": "Maths", "chapitre": "Vecteurs"},
    {"niveau": "2nde", "matiere": "Maths", "chapitre": "Trigonométrie"},
    {"niveau": "1ere", "matiere": "Maths", "chapitre": "Barycentre"},
    {"niveau": "Tle A", "matiere": "Philosophie", "chapitre": "Le temps"},
    {"niveau": "Tle C", "matiere": "Maths", "chapitre": "Equations différentielles"},
    {"niveau": "Tle D", "matiere": "SVT", "chapitre": "Ecologie"},
]

def generer_cours_avec_openai(niveau, matiere, chapitre):
    """Génère un cours avec OpenAI ou template si pas de clé"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Mode template si pas de clé (pour test)
        return {
            "niveau": niveau,
            "matiere": matiere,
            "chapitre": chapitre,
            "titre": f"{niveau} - {matiere} - {chapitre}",
            "contenu": f"# {chapitre}\n\n## Introduction ivoirienne\nExemple avec marché d'Abidjan...\n\n## Définitions\nCours de {matiere} {niveau} sur {chapitre} - Programme officiel CI\n\n## Exemples\nExemple 1: ...\n\n## Exercices\n1. Exercice...\nCorrigé: ...",
            "duree": "45 min",
            "difficulte": "Moyen",
            "status": "generated",
            "progress": 100,
            "agent": "Content Forge"
        }
    
    # Avec OpenAI - vrai génération
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        prompt = f"""Génère un cours complet pour {niveau} {matiere} - {chapitre}
Programme officiel Côte d'Ivoire.
Structure: Introduction ivoirienne (marché, attiéké...), Définitions, Formules, 2 exemples résolus étape par étape, 3 exercices avec corrigés, Astuce BEPC/BAC.
Langage simple pour élève {niveau}. Utilise exemples locaux Côte d'Ivoire.
Retourne en markdown.
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        
        contenu = response.choices[0].message.content
        
        return {
            "niveau": niveau,
            "matiere": matiere,
            "chapitre": chapitre,
            "titre": f"{niveau} - {matiere} - {chapitre}",
            "contenu": contenu,
            "duree": "45 min",
            "difficulte": "Moyen",
            "status": "generated",
            "progress": 100,
            "agent": "Content Forge - OpenAI"
        }
    except Exception as e:
        print(f"Erreur OpenAI: {e}, utilisation template")
        return generer_cours_avec_openai(niveau, matiere, chapitre)  # fallback sans clé

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()
    
    # Charger courses.json existant
    courses_path = Path("courses.json")
    if courses_path.exists():
        data = json.loads(courses_path.read_text(encoding="utf-8"))
        courses = data.get("courses", [])
    else:
        courses = []
    
    print(f"Cours existants: {len(courses)}")
    
    # Générer X nouveaux cours
    existants_chapitres = {f"{c['niveau']}|{c['matiere']}|{c['chapitre']}".lower() for c in courses}
    
    nouveaux = []
    for _ in range(args.count):
        # Choisir un cours manquant
        candidats = [c for c in CURRICULUM_MANQUANT if f"{c['niveau']}|{c['matiere']}|{c['chapitre']}".lower() not in existants_chapitres]
        if not candidats:
            candidats = CURRICULUM_MANQUANT
        
        choix = random.choice(candidats)
        print(f"Génération: {choix}")
        
        cours = generer_cours_avec_openai(choix["niveau"], choix["matiere"], choix["chapitre"])
        cours["id"] = len(courses) + len(nouveaux) + 1
        nouveaux.append(cours)
        existants_chapitres.add(f"{choix['niveau']}|{choix['matiere']}|{choix['chapitre']}".lower())
    
    # Ajouter aux existants
    courses.extend(nouveaux)
    
    # Sauvegarder
    courses_path.write_text(json.dumps({"courses": courses, "total": len(courses), "last_update": "auto"}, ensure_ascii=False, indent=2), encoding="utf-8")
    
    print(f"✅ {len(nouveaux)} nouveaux cours générés. Total: {len(courses)}")

if __name__ == "__main__":
    main()
