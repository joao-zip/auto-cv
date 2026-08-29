import re
from typing import Dict, List, Set, Tuple

# Comprehensive tech and engineering taxonomy for ATS keyword matching
TECH_TAXONOMY = {
    # Languages
    "c#": [r"\bc#\b", r"\bcsharp\b", r"\.net\b"],
    "c++": [r"\bc\+\+\b", r"\bcpp\b"],
    "python": [r"\bpython\b", r"\bpython3\b"],
    "go": [r"\bgo\b", r"\bgolang\b"],
    "typescript": [r"\btypescript\b", r"\bts\b"],
    "javascript": [r"\bjavascript\b", r"\bjs\b", r"\bes6\b"],
    "java": [r"\bjava\b"],
    "sql": [r"\bsql\b", r"\bt-sql\b", r"\bpl/sql\b"],
    "c": [r"\bc\b"],
    
    # Frameworks & Libraries
    "asp.net core": [r"\basp\.net\b", r"\b\.net core\b", r"\basp\.net core\b", r"\bdotnet\b"],
    "entity framework": [r"\bentity framework\b", r"\bef core\b", r"\borm\b"],
    "vue.js": [r"\bvue\b", r"\bvue\.js\b", r"\bvue3\b"],
    "react": [r"\breact\b", r"\breact\.js\b"],
    "angular": [r"\bangular\b"],
    "astro": [r"\bastro\b", r"\bastro\.js\b"],
    "qt": [r"\bqt\b", r"\bqt5\b", r"\bqt6\b"],
    "fastapi": [r"\bfastapi\b"],
    "flask": [r"\bflask\b"],
    "django": [r"\bdjango\b"],
    "node.js": [r"\bnode\b", r"\bnode\.js\b"],
    "spring boot": [r"\bspring\b", r"\bspring boot\b"],

    # Cloud & DevOps
    "docker": [r"\bdocker\b", r"\bcontainers\b"],
    "kubernetes": [r"\bkubernetes\b", r"\bk8s\b"],
    "azure": [r"\bazure\b", r"\bazure functions\b", r"\bazure devops\b"],
    "aws": [r"\baws\b", r"\bamazon web services\b", r"\blambda\b"],
    "gcp": [r"\bgcp\b", r"\bgoogle cloud\b"],
    "ci/cd": [r"\bci/cd\b", r"\bci\b", r"\bcd\b", r"\bpipelines\b", r"\bgithub actions\b"],
    "git": [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b"],
    "linux": [r"\blinux\b", r"\bgnu/linux\b", r"\barch\b", r"\bbash\b", r"\bshell\b"],
    "rabbitmq": [r"\brabbitmq\b", r"\bqueues\b", r"\bmessaging\b", r"\bmessage broker\b", r"\bevent-driven\b"],
    "kafka": [r"\bkafka\b"],

    # Databases
    "sql server": [r"\bsql server\b", r"\bmssql\b"],
    "postgresql": [r"\bpostgresql\b", r"\bpostgres\b"],
    "mongodb": [r"\bmongodb\b", r"\bmongo\b", r"\bnosql\b"],
    "redis": [r"\bredis\b"],
    "sqlite": [r"\bsqlite\b"],

    # Architecture & Practices
    "ddd": [r"\bddd\b", r"\bdomain[- ]driven design\b"],
    "clean architecture": [r"\bclean architecture\b", r"\barquitetura limpa\b"],
    "clean code": [r"\bclean code\b", r"\bcódigo limpo\b"],
    "tdd": [r"\btdd\b", r"\btest[- ]driven development\b"],
    "unit testing": [r"\bunit tests?\b", r"\btestes unit[áa]rios\b", r"\bxunit\b", r"\bpytest\b"],
    "mutation testing": [r"\bmutation testing\b", r"\btestes de muta[çc][ãa]o\b"],
    "microservices": [r"\bmicroservices\b", r"\bmicroservi[çc]os\b"],
    "rest api": [r"\brest\b", r"\brestful\b", r"\bapi\b", r"\bapis\b"],
    "design patterns": [r"\bdesign patterns\b", r"\bpadr[õo]es de projeto\b"],
    "agile": [r"\bagile\b", r"\bscrum\b", r"\bkanban\b"],
    "distributed systems": [r"\bdistributed\b", r"\bsistemas distribu[íi]dos\b", r"\basync\b", r"\bass[íi]ncron[ao]\b"],
}

def extract_keywords_from_text(text: str) -> Set[str]:
    text_lower = text.lower()
    found = set()
    for tech, patterns in TECH_TAXONOMY.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                found.add(tech)
                break
    return found

def analyze_job_description(jd_text: str, candidate_skills: Set[str]) -> Dict:
    jd_keywords = extract_keywords_from_text(jd_text)
    
    if not jd_keywords:
        # Fallback if no specific keywords matched
        return {
            "match_score": 100.0,
            "matched_keywords": list(candidate_skills),
            "missing_keywords": [],
            "total_jd_keywords": 0,
        }
    
    matched = jd_keywords.intersection(candidate_skills)
    missing = jd_keywords.difference(candidate_skills)
    
    score = (len(matched) / len(jd_keywords)) * 100 if jd_keywords else 100.0
    
    return {
        "match_score": round(score, 1),
        "matched_keywords": sorted(list(matched)),
        "missing_keywords": sorted(list(missing)),
        "total_jd_keywords": len(jd_keywords),
    }
