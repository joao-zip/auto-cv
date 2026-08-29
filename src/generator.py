import os
import subprocess
import tempfile
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from src.ats_analyzer import extract_keywords_from_text, analyze_job_description

class CVGenerator:
    def __init__(self, profile_path: str = "data/profile.yaml"):
        self.profile_path = Path(profile_path)
        with open(self.profile_path, "r", encoding="utf-8") as f:
            self.data = yaml.safe_load(f)

    def get_candidate_all_keywords(self) -> Set[str]:
        text_blob = yaml.dump(self.data)
        return extract_keywords_from_text(text_blob)

    def _sanitize(self, text: str) -> str:
        if not text:
            return ""
        # Escape special Typst characters
        return text.replace("#", "\\#").replace("@", "\\@")

    def render_typst(
        self,
        lang: str = "pt",
        focus_tags: Optional[List[str]] = None,
        jd_keywords: Optional[Set[str]] = None,
    ) -> str:
        lang = lang.lower()
        if lang not in ("pt", "en"):
            lang = "pt"

        personal = self.data.get("personal", {})
        edu = self.data.get("education", {})
        exps = self.data.get("experience", [])
        projs = self.data.get("projects", [])
        skills_data = self.data.get("skills", {})
        awards = self.data.get("awards", {}).get(lang, [])

        headings = {
            "pt": {
                "edu": "Educação",
                "exp": "Experiência",
                "proj": "Projetos",
                "skills": "Habilidades",
                "awards": "Conquistas e Certificados",
                "relevant_courses": "Disciplinas relevantes:",
                "tech_stack": "Tech Stack:",
            },
            "en": {
                "edu": "Education",
                "exp": "Experience",
                "proj": "Projects",
                "skills": "Technical Skills",
                "awards": "Honors & Certifications",
                "relevant_courses": "Relevant Coursework:",
                "tech_stack": "Tech Stack:",
            },
        }[lang]

        # Contact line
        links = personal.get("links", [])
        links_typst = []
        for lk in links:
            url = lk["url"]
            name = lk["name"]
            links_typst.append(f'#link("{url}")[{name}]')
        
        email = personal.get("email", "")
        phone = personal.get("phone", "")
        loc = personal.get("location", {}).get(lang, "")

        contact_parts = []
        contact_parts.extend(links_typst)
        if email:
            contact_parts.append(f'#link("mailto:{email}")[{self._sanitize(email)}]')
        if phone:
            contact_parts.append(f'[{phone}]')
        if loc:
            contact_parts.append(f'[{loc}]')

        contact_line = " #text(fill: rgb(\"#64748b\"))[|] ".join(contact_parts)

        typ = []
        typ.append('// AutoCV Generated Document')
        typ.append('#set page(')
        typ.append('  paper: "a4",')
        typ.append('  margin: (x: 1.25cm, top: 0.95cm, bottom: 0.95cm),')
        typ.append(')')
        typ.append('')
        typ.append(f'#set text(font: ("DejaVu Serif", "FreeSerif", "Liberation Serif"), size: 9.0pt, lang: "{lang}")')
        typ.append('#set par(justify: true, leading: 0.44em)')
        typ.append('')
        typ.append('#let section_heading(title) = {')
        typ.append('  v(3.5pt)')
        typ.append('  text(size: 11.5pt, weight: "bold", fill: rgb("#0f172a"))[#title]')
        typ.append('  v(-4.5pt)')
        typ.append('  line(length: 100%, stroke: 0.5pt + rgb("#cbd5e1"))')
        typ.append('  v(1pt)')
        typ.append('}')
        typ.append('')
        
        # Header
        name = personal.get("name", "")
        typ.append(f'#align(center)[')
        typ.append(f'  #text(size: 19pt, weight: "bold", fill: rgb("#0f172a"))[{name}] \\')
        typ.append(f'  #v(1pt)')
        typ.append(f'  #text(size: 8.6pt)[{contact_line}]')
        typ.append(f']')
        typ.append('')

        # Education
        typ.append(f'#section_heading("{headings["edu"]}")')
        inst = edu.get("institution", "")
        degree = edu.get("degree", {}).get(lang, "")
        period = edu.get("period", {}).get(lang, "")
        edu_loc = edu.get("location", {}).get(lang, "")
        coursework = edu.get("coursework", {}).get(lang, "")

        typ.append(f'#grid(')
        typ.append(f'  columns: (1fr, auto),')
        typ.append(f'  align: (left, right),')
        typ.append(f'  [ *{inst}* \\ #text(style: "italic", size: 8.6pt)[{degree}] ],')
        typ.append(f'  [ #text(size: 8.6pt)[{period}] \\ #text(style: "italic", size: 8.2pt, fill: rgb("#64748b"))[{edu_loc}] ]')
        typ.append(f')')
        if coursework:
            typ.append(f'#v(-3pt)')
            typ.append(f'- #text(size: 8.6pt)[*{headings["relevant_courses"]}* {self._sanitize(coursework)}]')
        typ.append('')

        # Experience
        typ.append(f'#section_heading("{headings["exp"]}")')
        for exp in exps:
            comp = exp.get("company", "")
            role = exp.get("role", {}).get(lang, "")
            exp_period = exp.get("period", {}).get(lang, "")
            exp_loc = exp.get("location", {}).get(lang, "")
            tech_stack = [self._sanitize(t) for t in exp.get("tech_stack", [])]
            bullets = exp.get("bullets", [])

            typ.append(f'#grid(')
            typ.append(f'  columns: (1fr, auto),')
            typ.append(f'  align: (left, right),')
            typ.append(f'  [ *{comp}* \\ #text(style: "italic", size: 8.6pt)[{role}] ],')
            typ.append(f'  [ #text(size: 8.6pt)[{exp_period}] \\ #text(style: "italic", size: 8.2pt, fill: rgb("#64748b"))[{exp_loc}] ]')
            typ.append(f')')
            typ.append(f'#v(-4pt)')
            for b in bullets:
                b_text = b.get(lang, "")
                if b_text:
                    typ.append(f'- #text(size: 8.6pt)[{self._sanitize(b_text)}]')
            if tech_stack:
                typ.append(f'#v(-3pt)')
                typ.append(f'#text(size: 8.3pt)[*{headings["tech_stack"]}* {", ".join(tech_stack)}]')
            typ.append(f'#v(1pt)')
        typ.append('')

        # Projects
        typ.append(f'#section_heading("{headings["proj"]}")')
        for proj in projs:
            pname = proj.get("name", "")
            purl = proj.get("url", "")
            prole = proj.get("role", {}).get(lang, "")
            pperiod = proj.get("period", {}).get(lang, "")
            ptech = [self._sanitize(t) for t in proj.get("tech_stack", [])]
            pbullets = proj.get("bullets", [])

            title_render = f'#link("{purl}")[*{pname}*]' if purl else f'*{pname}*'

            typ.append(f'#grid(')
            typ.append(f'  columns: (1fr, auto),')
            typ.append(f'  align: (left, right),')
            typ.append(f'  [ {title_render} \\ #text(style: "italic", size: 8.6pt)[{prole}] ],')
            typ.append(f'  [ #text(size: 8.6pt)[{pperiod}] ]')
            typ.append(f')')
            typ.append(f'#v(-4pt)')
            for pb in pbullets:
                pb_text = pb.get(lang, "")
                if pb_text:
                    typ.append(f'- #text(size: 8.6pt)[{self._sanitize(pb_text)}]')
            if ptech:
                typ.append(f'#v(-3pt)')
                typ.append(f'#text(size: 8.3pt)[*{headings["tech_stack"]}* {", ".join(ptech)}]')
            typ.append(f'#v(1pt)')
        typ.append('')

        # Skills
        typ.append(f'#section_heading("{headings["skills"]}")')
        
        spoken = skills_data.get("languages_spoken", {}).get(lang, "")
        if spoken:
            label = "Idiomas:" if lang == "pt" else "Languages:"
            typ.append(f'- #text(size: 8.6pt)[*{label}* {self._sanitize(spoken)}]')

        langs = skills_data.get("languages", {}).get(lang, "")
        if langs:
            label = "Linguagens:" if lang == "pt" else "Programming Languages:"
            typ.append(f'- #text(size: 8.6pt)[*{label}* {self._sanitize(langs)}]')

        fw = skills_data.get("frameworks_tech", {}).get(lang, "")
        if fw:
            label = "Tecnologias & Frameworks:" if lang == "pt" else "Technologies & Frameworks:"
            typ.append(f'- #text(size: 8.6pt)[*{label}* {self._sanitize(fw)}]')

        db = skills_data.get("databases", {}).get(lang, "")
        if db:
            label = "Bancos de Dados:" if lang == "pt" else "Databases:"
            typ.append(f'- #text(size: 8.6pt)[*{label}* {self._sanitize(db)}]')

        practices = skills_data.get("practices", {}).get(lang, "")
        if practices:
            label = "Práticas & Metodologias:" if lang == "pt" else "Engineering Practices:"
            typ.append(f'- #text(size: 8.6pt)[*{label}* {self._sanitize(practices)}]')

        devops = skills_data.get("technologies", {}).get(lang, "")
        if devops:
            label = "DevOps & Ferramentas:" if lang == "pt" else "DevOps & Tools:"
            typ.append(f'- #text(size: 8.6pt)[*{label}* {self._sanitize(devops)}]')

        typ.append('')

        # Awards & Certifications
        if awards:
            typ.append(f'#section_heading("{headings["awards"]}")')
            for aw in awards:
                typ.append(f'- #text(size: 8.6pt)[{self._sanitize(aw)}]')

        return "\n".join(typ)

    def compile(self, typst_content: str, output_pdf_path: str) -> bool:
        out_path = Path(output_pdf_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        with tempfile.NamedTemporaryFile(suffix=".typ", mode="w", encoding="utf-8", delete=False) as tmp:
            tmp.write(typst_content)
            tmp_path = tmp.name

        try:
            cmd = ["typst", "compile", tmp_path, str(out_path.resolve())]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error compiling Typst: {e.stderr}")
            return False
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
