import os
import subprocess
import tempfile
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set
from src.ats_analyzer import extract_keywords_from_text, analyze_job_description, score_item_relevance

class CVGenerator:
    def __init__(self, profile_path: str = "data/profile.yaml", fonts_path: str = "fonts"):
        self.profile_path = Path(profile_path)
        self.fonts_path = Path(fonts_path)
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
        max_bullets_per_exp: Optional[int] = None,
        selected_project_ids: Optional[List[str]] = None,
        selected_bullet_ids: Optional[List[str]] = None,
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

        # Contact line with icons
        links = personal.get("links", [])
        icon_map = {
            "linkedin": "#fa-linkedin()",
            "github": "#fa-github()",
            "site": "#fa-globe()",
        }

        contact_parts = []
        for lk in links:
            url = lk["url"]
            name = lk["name"]
            icon = icon_map.get(name.lower(), "#fa-link()")
            contact_parts.append(f'#link("{url}")[{icon} {name}]')
        
        email = personal.get("email", "")
        phone = personal.get("phone", "")

        if email:
            contact_parts.append(f'#link("mailto:{email}")[#fa-envelope() {self._sanitize(email)}]')
        if phone:
            contact_parts.append(f'#fa-phone() {phone}')

        contact_line = " #h(10pt) ".join(contact_parts)

        typ = []
        typ.append('// AutoCV Generated Document')
        typ.append('#import "@preview/fontawesome:0.5.0": *')
        typ.append('')
        typ.append('#set page(')
        typ.append('  paper: "a4",')
        typ.append('  margin: (x: 1.25cm, top: 0.85cm, bottom: 0.85cm),')
        typ.append(')')
        typ.append('')
        typ.append(f'#set text(font: ("Crimson Pro", "Libertinus Serif", "DejaVu Serif"), size: 10.5pt, lang: "{lang}", hyphenate: false)')
        typ.append('#set par(justify: false, leading: 0.43em)')
        typ.append('')
        typ.append('#let section_heading(title) = {')
        typ.append('  v(3.5pt)')
        typ.append('  text(size: 13.8pt, weight: "bold", fill: rgb("#0f172a"))[#title]')
        typ.append('  v(-4pt)')
        typ.append('  line(length: 100%, stroke: 0.5pt + rgb("#94a3b8"))')
        typ.append('  v(1.5pt)')
        typ.append('}')
        typ.append('')
        typ.append('#let ext_link(url, content) = {')
        typ.append('  link(url)[#content #text(size: 8pt, fill: rgb("#475569"))[#fa-arrow-up-right-from-square(size: 7pt)]]')
        typ.append('}')
        typ.append('')
        
        # Header - Left aligned
        name = personal.get("name", "")
        typ.append(f'#align(left)[')
        typ.append(f'  #text(size: 24pt, weight: "bold", fill: rgb("#0f172a"))[{name}] \\')
        typ.append(f'  #v(2.5pt)')
        typ.append(f'  #text(size: 9.8pt)[{contact_line}]')
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
        typ.append(f'  [ *{inst}* \\ #text(style: "italic", size: 10pt)[{degree}] ],')
        typ.append(f'  [ #text(size: 10pt)[{period}] \\ #text(style: "italic", size: 9.4pt, fill: rgb("#64748b"))[{edu_loc}] ]')
        typ.append(f')')
        if coursework:
            typ.append(f'#v(-2.5pt)')
            typ.append(f'- #text(size: 10.1pt)[*{headings["relevant_courses"]}* {self._sanitize(coursework)}]')
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

            scored_bullets = []
            for b in bullets:
                b_id = b.get("id", "")
                if selected_bullet_ids and b_id not in selected_bullet_ids:
                    continue
                b_tags = b.get("tags", [])
                score = score_item_relevance(b_tags, jd_keywords or set())
                b_text = b.get(lang, "")
                if b_text:
                    scored_bullets.append((score, b_text))

            if jd_keywords:
                scored_bullets.sort(key=lambda x: x[0], reverse=True)
            
            if max_bullets_per_exp and max_bullets_per_exp > 0:
                scored_bullets = scored_bullets[:max_bullets_per_exp]

            typ.append(f'#grid(')
            typ.append(f'  columns: (1fr, auto),')
            typ.append(f'  align: (left, right),')
            typ.append(f'  [ *{comp}* \\ #text(style: "italic", size: 10pt)[{role}] ],')
            typ.append(f'  [ #text(size: 10pt)[{exp_period}] \\ #text(style: "italic", size: 9.4pt, fill: rgb("#64748b"))[{exp_loc}] ]')
            typ.append(f')')
            typ.append(f'#v(-3.5pt)')
            for _, b_text in scored_bullets:
                typ.append(f'- #text(size: 10.1pt)[{self._sanitize(b_text)}]')
            if tech_stack:
                typ.append(f'#v(-2.5pt)')
                typ.append(f'#text(size: 9.6pt)[*{headings["tech_stack"]}* {", ".join(tech_stack)}]')
            typ.append(f'#v(1.5pt)')
        typ.append('')

        # Projects (with intelligent ranking, default_visible, and selection)
        typ.append(f'#section_heading("{headings["proj"]}")')
        scored_projs = []
        for proj in projs:
            p_id = proj.get("id", "")
            is_default = proj.get("default_visible", True)

            if selected_project_ids is not None:
                if p_id not in selected_project_ids:
                    continue
            elif not is_default:
                if not jd_keywords:
                    continue
                score = score_item_relevance(proj.get("tags", []), jd_keywords)
                if score <= 1:
                    continue

            p_tags = proj.get("tags", [])
            score = score_item_relevance(p_tags, jd_keywords or set())
            scored_projs.append((score, proj))

        if jd_keywords:
            scored_projs.sort(key=lambda x: x[0], reverse=True)

        for _, proj in scored_projs:
            pname = proj.get("name", "")
            purl = proj.get("url", "")
            prole = proj.get("role", {}).get(lang, "")
            pperiod = proj.get("period", {}).get(lang, "")
            ptech = [self._sanitize(t) for t in proj.get("tech_stack", [])]
            pbullets = proj.get("bullets", [])

            title_render = f'#ext_link("{purl}", [*{pname}*])' if purl else f'*{pname}*'

            typ.append(f'#grid(')
            typ.append(f'  columns: (1fr, auto),')
            typ.append(f'  align: (left, right),')
            typ.append(f'  [ {title_render} \\ #text(style: "italic", size: 10pt)[{prole}] ],')
            typ.append(f'  [ #text(size: 10pt)[{pperiod}] ]')
            typ.append(f')')
            typ.append(f'#v(-3.5pt)')
            for pb in pbullets:
                pb_text = pb.get(lang, "")
                if pb_text:
                    typ.append(f'- #text(size: 10.1pt)[{self._sanitize(pb_text)}]')
            if ptech:
                typ.append(f'#v(-2.5pt)')
                typ.append(f'#text(size: 9.6pt)[*{headings["tech_stack"]}* {", ".join(ptech)}]')
            typ.append(f'#v(1.5pt)')
        typ.append('')

        # Skills
        typ.append(f'#section_heading("{headings["skills"]}")')
        
        spoken_data = skills_data.get("languages_spoken", {}).get(lang, {})
        label_lang = "Idiomas:" if lang == "pt" else "Languages:"
        if isinstance(spoken_data, dict):
            stext = spoken_data.get("text", "")
            cname = spoken_data.get("cert_name", "")
            curl = spoken_data.get("cert_url", "")
            extra = spoken_data.get("extra", "")
            cert_part = f'#ext_link("{curl}", [{cname}])' if curl else cname
            typ.append(f'- #text(size: 10.1pt)[*{label_lang}* {stext} ({cert_part}) {extra}]')
        elif spoken_data:
            typ.append(f'- #text(size: 10.1pt)[*{label_lang}* {self._sanitize(str(spoken_data))}]')

        langs = skills_data.get("languages", {}).get(lang, "")
        if langs:
            label = "Linguagens:" if lang == "pt" else "Programming Languages:"
            typ.append(f'- #text(size: 10.1pt)[*{label}* {self._sanitize(langs)}]')

        fw = skills_data.get("frameworks_tech", {}).get(lang, "")
        if fw:
            label = "Tecnologias & Frameworks:" if lang == "pt" else "Technologies & Frameworks:"
            typ.append(f'- #text(size: 10.1pt)[*{label}* {self._sanitize(fw)}]')

        db = skills_data.get("databases", {}).get(lang, "")
        if db:
            label = "Bancos de Dados:" if lang == "pt" else "Databases:"
            typ.append(f'- #text(size: 10.1pt)[*{label}* {self._sanitize(db)}]')

        practices = skills_data.get("practices", {}).get(lang, "")
        if practices:
            label = "Práticas & Metodologias:" if lang == "pt" else "Engineering Practices:"
            typ.append(f'- #text(size: 10.1pt)[*{label}* {self._sanitize(practices)}]')

        devops = skills_data.get("technologies", {}).get(lang, "")
        if devops:
            label = "DevOps & Ferramentas:" if lang == "pt" else "DevOps & Tools:"
            typ.append(f'- #text(size: 10.1pt)[*{label}* {self._sanitize(devops)}]')

        typ.append('')

        # Awards & Certifications
        if awards:
            typ.append(f'#section_heading("{headings["awards"]}")')
            for aw in awards:
                if isinstance(aw, dict):
                    atext = self._sanitize(aw.get("text", ""))
                    aurl = aw.get("url", "")
                    if aurl:
                        typ.append(f'- #text(size: 10.1pt)[#ext_link("{aurl}", [{atext}]) ]')
                    else:
                        typ.append(f'- #text(size: 10.1pt)[{atext}]')
                else:
                    typ.append(f'- #text(size: 10.1pt)[{self._sanitize(str(aw))}]')

        return "\n".join(typ)

    def compile(self, typst_content: str, output_pdf_path: str) -> bool:
        out_path = Path(output_pdf_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        with tempfile.NamedTemporaryFile(suffix=".typ", mode="w", encoding="utf-8", delete=False) as tmp:
            tmp.write(typst_content)
            tmp_path = tmp.name

        try:
            cmd = ["typst", "compile"]
            if self.fonts_path.exists():
                cmd.extend(["--font-path", str(self.fonts_path.resolve())])
            cmd.extend([tmp_path, str(out_path.resolve())])
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error compiling Typst: {e.stderr}")
            return False
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
