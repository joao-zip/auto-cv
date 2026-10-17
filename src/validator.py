"""
Validator for profile.yaml schema integrity.
Ensures required fields, bilingual parity (pt/en), and structure are correct.
"""
from pathlib import Path
from typing import Any, Dict, List, Tuple
import yaml


class ValidationError(Exception):
    def __init__(self, errors: List[str]):
        self.errors = errors
        super().__init__("\n".join(errors))


def _check_bilingual(data: Any, path: str, errors: List[str], required: bool = True):
    if not isinstance(data, dict):
        if required:
            errors.append(f"[{path}] must be a bilingual dictionary with 'pt' and 'en' keys, got: {type(data).__name__}")
        return
    for lang in ("pt", "en"):
        val = data.get(lang)
        if not val or not isinstance(val, (str, dict, list)):
            errors.append(f"[{path}.{lang}] missing or empty")
        elif isinstance(val, str) and not val.strip():
            errors.append(f"[{path}.{lang}] cannot be empty string")


def validate_profile_dict(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if not isinstance(data, dict):
        return False, ["Profile root must be a YAML mapping/dictionary."]

    # 1. Personal section
    personal = data.get("personal")
    if not isinstance(personal, dict):
        errors.append("[personal] section is missing or not a dictionary")
    else:
        for field in ("name", "email", "phone"):
            val = personal.get(field)
            if not val or not isinstance(val, str) or not val.strip():
                errors.append(f"[personal.{field}] is missing or empty")
        
        links = personal.get("links", [])
        if not isinstance(links, list) or len(links) == 0:
            errors.append("[personal.links] must be a non-empty list")
        else:
            for i, link in enumerate(links):
                if not isinstance(link, dict):
                    errors.append(f"[personal.links[{i}]] must be a dictionary")
                    continue
                for lk in ("name", "url", "display"):
                    if not link.get(lk):
                        errors.append(f"[personal.links[{i}].{lk}] is missing or empty")

    # 2. Education section
    education = data.get("education")
    if not isinstance(education, dict):
        errors.append("[education] section is missing or not a dictionary")
    else:
        if not education.get("institution"):
            errors.append("[education.institution] is missing or empty")
        _check_bilingual(education.get("degree"), "education.degree", errors)
        _check_bilingual(education.get("period"), "education.period", errors)
        _check_bilingual(education.get("location"), "education.location", errors)

    # 3. Experience section
    experiences = data.get("experience")
    if not isinstance(experiences, list):
        errors.append("[experience] section must be a list")
    else:
        for i, exp in enumerate(experiences):
            exp_id = exp.get("id", f"index_{i}") if isinstance(exp, dict) else f"index_{i}"
            prefix = f"experience[{exp_id}]"
            if not isinstance(exp, dict):
                errors.append(f"[{prefix}] must be a dictionary")
                continue
            if not exp.get("company"):
                errors.append(f"[{prefix}.company] is missing or empty")
            _check_bilingual(exp.get("role"), f"{prefix}.role", errors)
            _check_bilingual(exp.get("period"), f"{prefix}.period", errors)
            _check_bilingual(exp.get("location"), f"{prefix}.location", errors)
            
            tech_stack = exp.get("tech_stack")
            if not isinstance(tech_stack, list) or len(tech_stack) == 0:
                errors.append(f"[{prefix}.tech_stack] must be a non-empty list of technologies")
            
            bullets = exp.get("bullets")
            if not isinstance(bullets, list) or len(bullets) == 0:
                errors.append(f"[{prefix}.bullets] must be a non-empty list")
            else:
                for j, bullet in enumerate(bullets):
                    b_id = bullet.get("id", f"b_{j}") if isinstance(bullet, dict) else f"b_{j}"
                    b_prefix = f"{prefix}.bullets[{b_id}]"
                    if not isinstance(bullet, dict):
                        errors.append(f"[{b_prefix}] must be a dictionary")
                        continue
                    if not isinstance(bullet.get("tags"), list) or len(bullet.get("tags")) == 0:
                        errors.append(f"[{b_prefix}.tags] must be a non-empty list of tags")
                    _check_bilingual(bullet, b_prefix, errors)

    # 4. Leadership / Community section (optional)
    leadership = data.get("leadership", [])
    if leadership and isinstance(leadership, list):
        for i, lead in enumerate(leadership):
            l_id = lead.get("id", f"lead_{i}") if isinstance(lead, dict) else f"lead_{i}"
            prefix = f"leadership[{l_id}]"
            if not isinstance(lead, dict):
                errors.append(f"[{prefix}] must be a dictionary")
                continue
            org = lead.get("name") or lead.get("organization")
            if not org:
                errors.append(f"[{prefix}.name] is missing or empty")
            elif isinstance(org, dict):
                _check_bilingual(org, f"{prefix}.name", errors)
            _check_bilingual(lead.get("role"), f"{prefix}.role", errors)
            _check_bilingual(lead.get("period"), f"{prefix}.period", errors)

    # 5. Projects section (optional list)
    projects = data.get("projects", [])
    if not isinstance(projects, list):
        errors.append("[projects] must be a list if present")
    else:
        for i, proj in enumerate(projects):
            p_id = proj.get("id", f"proj_{i}") if isinstance(proj, dict) else f"proj_{i}"
            prefix = f"projects[{p_id}]"
            if not isinstance(proj, dict):
                errors.append(f"[{prefix}] must be a dictionary")
                continue
            if not proj.get("name"):
                errors.append(f"[{prefix}.name] is missing or empty")
            _check_bilingual(proj.get("role"), f"{prefix}.role", errors)
            bullets = proj.get("bullets")
            if not isinstance(bullets, list) or len(bullets) == 0:
                errors.append(f"[{prefix}.bullets] must be a non-empty list of bilingual bullets")
            else:
                for j, bullet in enumerate(bullets):
                    b_prefix = f"{prefix}.bullets[{j}]"
                    _check_bilingual(bullet, b_prefix, errors)

    # 6. Skills section
    skills = data.get("skills")
    if not isinstance(skills, dict):
        errors.append("[skills] section is missing or not a dictionary")
    else:
        for cat in ("languages", "frameworks_tech", "databases", "practices", "technologies"):
            if cat in skills:
                _check_bilingual(skills.get(cat), f"skills.{cat}", errors)
            else:
                errors.append(f"[skills.{cat}] is missing")

    # 7. Awards section (optional)
    awards = data.get("awards")
    if awards:
        if not isinstance(awards, dict):
            errors.append("[awards] must be a dictionary with 'pt' and 'en' lists")
        else:
            for lang in ("pt", "en"):
                if lang in awards and not isinstance(awards[lang], list):
                    errors.append(f"[awards.{lang}] must be a list of items")

    return (len(errors) == 0, errors)


def validate_profile_file(filepath: Path | str) -> Tuple[bool, List[str]]:
    path = Path(filepath)
    if not path.exists():
        return False, [f"File not found: {path}"]
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        return False, [f"Failed to parse YAML in {path}: {str(e)}"]

    return validate_profile_dict(data)
