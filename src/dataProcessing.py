import os
import subprocess
import requests
from dotenv import load_dotenv
import fitz
import pickle



load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"token {GITHUB_TOKEN}"}


#################################################################################
# GitHub cloning functions

def get_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def clone_repo(repo_name):
    repo_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}.git"
    target_dir = f"../data/github_projects/{repo_name}"
    if not os.path.exists(target_dir):
        print(f"Cloning {repo_name}...")
        subprocess.run(["git", "clone", repo_url, target_dir])
    else:
        print(f"{repo_name} already cloned.")

def clone_all_repos():
    repos = get_repos(GITHUB_USERNAME)
    for repo in repos:
        clone_repo(repo['name'])

#################################################################################
# File extraction settings and functions

RELEVANT_EXTENSIONS = {
    '.py', '.js', '.ts', '.java', '.cpp',
    '.md', '.json', '.yaml', '.yml',
    '.sh', '.bat', '.html', '.ipynb'
}

EXCLUDE_FOLDERS = {
    '.git', 'node_modules', 'build', 'dist', '__pycache__'
}

def is_relevant_file(filename):
    _, ext = os.path.splitext(filename)
    return ext.lower() in RELEVANT_EXTENSIONS

def extract_texts(base_dir):
    all_texts = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS]
        for file in files:
            if is_relevant_file(file):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text = f.read()
                        if text.strip():
                            all_texts.append((filepath, text))
                except Exception as e:
                    print(f"Skipping {filepath}, error: {e}")
    return all_texts


#################################################################################
# Extracting text from CV pdf

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text.strip()
    except Exception as e:
        print(f"Failed to extract PDF text from {pdf_path}: {e}")
        return ""
    

def extract_texts_from_pdfs(cv_dir):
    texts = []
    for filename in os.listdir(cv_dir):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(cv_dir, filename)
            text = extract_text_from_pdf(filepath)
            if text:
                texts.append((filepath, text))
                print(f"Extracted text from {filename}")
            else:
                print(f"No text extracted from {filename}")
    return texts







if __name__ == "__main__":
    os.makedirs("../data/github_projects", exist_ok=True)
    github_base_dir = os.path.expanduser("~/personalRagChatbot/data/github_projects")
    cv_dir = os.path.expanduser("~/personalRagChatbot/data/pdfs")

    # Clone GitHub and extract texts
    clone_all_repos()
    data = extract_texts(github_base_dir)

    # Extract all CV/thesis/paper texts
    if os.path.exists(cv_dir):
        cv_texts = extract_texts_from_pdfs(cv_dir)
        data.extend(cv_texts)
    else:
        print(f"CV directory not found: {cv_dir}")

    # for filepath, text in data:
    #     print(f"\n File: {filepath}")
    #     print(f" Length: {len(text)} characters")
    #     print(f" Preview:\n{text[:300]}...\n{'-'*80}")
    
    with open('../data/processed/raw_data.pkl', 'wb') as f:
        pickle.dump(data, f)
    print(f"Extracted text from {len(data)} files including GitHub and PDF documents.")

