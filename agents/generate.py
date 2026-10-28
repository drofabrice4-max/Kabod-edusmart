import os
import json
import random
from datetime import datetime

def generer_cours_template(niveau, matiere, chapitre):
    """Génère un cours sans OpenAI - mode template avec figures"""
    exercices = [
        {"enonce": f"Exercice 1: Calcule {chapitre} avec les données du marché d'Adjamé", "solution": "Solution détaillée étape par étape avec exemple ivoirien"},
        {"enonce": f"Exercice 2: Application pratique de {chapitre}", "solution": "Résolution avec schéma"},
        {"enonce": f"Exercice 3: Problème complexe sur {chapitre}", "solution": "Méthode + astuce BEPC/BAC"},
    ]
    
    figures_svg = f'''<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="300" height="200" fill="#DBEAFE" rx="10"/><text x="150" y="100" text-anchor="middle" font-size="14" fill="#1e40af">{chapitre}</text><polygon points="50,150 150,50 250,150" fill="#BBF7D0" stroke="#166534" stroke-width="2"/></svg>'''
    
    contenu = f"""
    <h2>{chapitre} - {matiere} {niveau}</h2>
    <div style="background:#DBEAFE;padding:12px;border-radius:10px;margin:10px 0">
    <p><b>Définition :</b> {chapitre} est un concept clé du programme ivoirien.</p>
    </div>
    {figures_svg}
    <h3>📚 Cours détaillé</h3>
    <p>Exemple du marché d'Abidjan : Si un commerçant vend de l'attiéké...</p>
    <div style="background:#DCFCE7;padding:12px;border-radius:10px;margin:10px 0">
    <p><b>Formule :</b> Application pratique avec données ivoiriennes</p>
    </div>
    <h3>✏️ Série d'exercices (5 exercices)</h3>
    <div style="background:#FEF3C7;padding:10px;border-radius:8px;margin:5px 0"><b>Ex 1:</b> {exercices[0]['enonce']}<br><b>Solution:</b> {exercices[0]['solution']}</div>
    <div style="background:#FCE7F3;padding:10px;border-radius:8px;margin:5px 0"><b>Ex 2:</b> {exercices[1]['enonce']}<br><b>Solution:</b> {exercices[1]['solution']}</div>
    <div style="background:#E9D5FF;padding:10px;border-radius:8px;margin:5px 0"><b>Ex 3:</b> {exercices[2]['enonce']}<br><b>Solution:</b> {exercices[2]['solution']}</div>
    <h3>🎯 Pour retenir</h3>
    <ul><li>{chapitre} - astuce BEPC</li><li>Exemple Adjamé</li><li>Formule à retenir</li></ul>
    """
    
    return {
        "id": f"{niveau}-{matiere}-{random.randint(1000,9999)}",
        "niveau": niveau,
        "matiere": matiere,
        "titre": chapitre,
        "chapitre": chapitre,
        "contenu": contenu,
        "duree": "45 min",
        "difficulte": random.choice(["Facile", "Moyen", "Difficile"]),
        "date": datetime.now().isoformat()
    }

def generer_cours_avec_openai(niveau, matiere, chapitre):
    """Essaie OpenAI, sinon fallback template SANS RECURSION"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print(f"Pas de clé OpenAI, mode template pour {chapitre}")
        return generer_cours_template(niveau, matiere, chapitre)
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"Génère un cours détaillé de {matiere} {niveau} sur {chapitre} avec 5 exercices, figures SVG, exemples ivoiriens (marché Adjamé, attiéké), programme CI"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            timeout=30
        )
        contenu = response.choices[0].message.content
        return {
            "id": f"{niveau}-{matiere}-{random.randint(1000,9999)}",
            "niveau": niveau,
            "matiere": matiere,
            "titre": chapitre,
            "chapitre": chapitre,
            "contenu": contenu,
            "duree": "45 min",
            "difficulte": "Moyen",
            "date": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Erreur OpenAI {e}, fallback template")
        return generer_cours_template(niveau, matiere, chapitre)

def main():
    count = 3
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=3)
    args = parser.parse_args()
    count = args.count
    
    print(f"Génération de {count} cours...")
    
    try:
        with open("courses.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            courses = data.get("courses", [])
    except:
        courses = []
    
    niveaux = ["6e", "5e", "4e", "3e", "2nde", "1ere", "Tle A", "Tle C", "Tle D"]
    matieres = ["Maths", "Physique", "SVT", "Français", "Anglais", "Histoire-Géo"]
    chapitres = ["Pythagore - Figures colorées", "Vecteurs et translation", "Équations quadratiques", "Thalès avec figures", "Fonctions avec graphiques", "Élasticité avec schémas"]
    
    for i in range(count):
        niveau = random.choice(niveaux)
        matiere = random.choice(matieres)
        chapitre = random.choice(chapitres)
        cours = generer_cours_avec_openai(niveau, matiere, chapitre)
        courses.append(cours)
        print(f"Cours {i+1}/{count}: {chapitre} OK")
    
    with open("courses.json", "w", encoding="utf-8") as f:
        json.dump({"courses": courses, "total": len(courses), "updated": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    
    print(f"Total: {len(courses)} cours")

if __name__ == "__main__":
    main()
