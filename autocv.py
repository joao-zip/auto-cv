#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from src.generator import CVGenerator
from src.ats_analyzer import analyze_job_description, extract_keywords_from_text

def cmd_generate(args):
    gen = CVGenerator(args.profile)
    typ_source = gen.render_typst(lang=args.lang)
    output_pdf = args.output or f"output/CV_Joao_Oliveira_{args.lang.upper()}.pdf"
    
    success = gen.compile(typ_source, output_pdf)
    if success:
        print(f"[SUCCESS] CV generated: {output_pdf}")
    else:
        print(f"[ERROR] Failed to compile CV.")
        sys.exit(1)

def cmd_tailor(args):
    gen = CVGenerator(args.profile)
    jd_text = ""
    if args.jd:
        jd_path = Path(args.jd)
        if jd_path.exists():
            with open(jd_path, "r", encoding="utf-8") as f:
                jd_text = f.read()
        else:
            jd_text = args.jd
    elif args.jd_text:
        jd_text = args.jd_text
    else:
        print("[ERROR] Please provide a Job Description via --jd <file_or_text> or --jd-text '<text>'")
        sys.exit(1)

    candidate_skills = gen.get_candidate_all_keywords()
    ats_report = analyze_job_description(jd_text, candidate_skills)
    
    company_slug = args.company.strip().replace(" ", "_") if args.company else "Custom"
    output_pdf = args.output or f"output/CV_Joao_Oliveira_{company_slug}_{args.lang.upper()}.pdf"

    typ_source = gen.render_typst(
        lang=args.lang,
        jd_keywords=set(ats_report["matched_keywords"]),
    )
    
    success = gen.compile(typ_source, output_pdf)
    if success:
        print(f"\n=======================================================")
        print(f"ATS Analysis & Tailoring Report - {company_slug}")
        print(f"=======================================================")
        print(f"ATS Match Score: {ats_report['match_score']}%")
        print(f"Matched Keywords ({len(ats_report['matched_keywords'])}): {', '.join(ats_report['matched_keywords']) if ats_report['matched_keywords'] else 'None'}")
        if ats_report['missing_keywords']:
            print(f"Missing / Unmatched Keywords ({len(ats_report['missing_keywords'])}): {', '.join(ats_report['missing_keywords'])}")
            print(f"Suggestion: Consider adding project experience or coursework covering these if applicable.")
        print(f"Output PDF generated: {output_pdf}")
        print(f"=======================================================\n")
    else:
        print("[ERROR] Failed to compile tailored CV.")
        sys.exit(1)

def cmd_score(args):
    gen = CVGenerator(args.profile)
    jd_path = Path(args.jd)
    if jd_path.exists():
        with open(jd_path, "r", encoding="utf-8") as f:
            jd_text = f.read()
    else:
        jd_text = args.jd

    candidate_skills = gen.get_candidate_all_keywords()
    ats_report = analyze_job_description(jd_text, candidate_skills)

    print(f"\n=======================================================")
    print(f"ATS Compatibility Scorer")
    print(f"=======================================================")
    print(f"Match Score: {ats_report['match_score']}%")
    print(f"Matched Keywords ({len(ats_report['matched_keywords'])}): {', '.join(ats_report['matched_keywords'])}")
    print(f"Missing Keywords ({len(ats_report['missing_keywords'])}): {', '.join(ats_report['missing_keywords']) if ats_report['missing_keywords'] else 'None'}")
    print(f"=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="AutoCV: Automated ATS-friendly CV Generator & Tailoring Tool")
    parser.add_argument("--profile", default="data/profile.yaml", help="Path to profile.yaml data file")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate
    p_gen = subparsers.add_parser("generate", help="Generate standard CV in PT or EN")
    p_gen.add_argument("--lang", choices=["pt", "en"], default="pt", help="Language for the CV (default: pt)")
    p_gen.add_argument("--output", "-o", help="Custom output PDF path")

    # Tailor
    p_tailor = subparsers.add_parser("tailor", help="Tailor CV to a specific Job Description")
    p_tailor.add_argument("--jd", help="Path to job description file or raw JD text")
    p_tailor.add_argument("--jd-text", help="Raw job description text string")
    p_tailor.add_argument("--lang", choices=["pt", "en"], default="en", help="Language for the CV (default: en)")
    p_tailor.add_argument("--company", "-c", help="Company name (for file naming and tagging)")
    p_tailor.add_argument("--output", "-o", help="Custom output PDF path")

    # Score
    p_score = subparsers.add_parser("score", help="Score profile compatibility against a Job Description")
    p_score.add_argument("--jd", required=True, help="Path to job description file or raw text")

    args = parser.parse_args()
    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "tailor":
        cmd_tailor(args)
    elif args.command == "score":
        cmd_score(args)

if __name__ == "__main__":
    main()
