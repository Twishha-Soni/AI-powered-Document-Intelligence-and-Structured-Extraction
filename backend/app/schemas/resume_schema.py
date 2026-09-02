from pydantic import BaseModel, Field, model_validator
from typing import Literal
import re

from app.schemas.base_schema import ExtractedDocument


class ContactInfo(BaseModel):
    email: str | None = Field(default=None, description="Candidate's email address, if present.")
    phone: str | None = Field(default=None, description="Candidate's phone number, if present.")
    location: str | None = Field(default=None, description="City/region as stated on the resume, if present (resumes rarely give a full street address).")
    linkedin_url: str | None = Field(default=None, description="LinkedIn profile URL, if present.")
    github_url: str | None = Field(default=None, description="GitHub profile URL, if present.")
    portfolio_url: str | None = Field(default=None, description="Personal website or portfolio URL, if present.")
    other_links: list[str] = Field(default_factory=list, description="Any other listed URLs not captured above (Twitter, Behance, publications, etc.).")


class WorkExperience(BaseModel):
    job_title: str = Field(description="Job title/role held.")
    company_name: str = Field(description="Name of the employer.")
    location: str | None = Field(default=None, description="Job location (city, state/country, or 'Remote'), if present.")
    start_date: str = Field(description="Start date as printed on the resume, e.g. 'Jan 2021', '2021', '06/2021'. Kept as free text since resumes vary in date precision/format.")
    end_date: str | None = Field(default=None, description="End date as printed on the resume, in the same free-text style. None if not stated.")
    is_current: bool = Field(default=False, description="Whether this is the candidate's current position (e.g. end date says 'Present').")
    description: str | None = Field(default=None, description="Overall role summary, if given separately from bullet points.")
    responsibilities: list[str] = Field(default_factory=list, description="Bullet points describing responsibilities and achievements in this role.")


class Education(BaseModel):
    degree: str | None = Field(default=None, description="Degree name, e.g. 'B.Tech in Computer Engineering'. None if only an institution is listed (e.g. a certification-only entry).")
    field_of_study: str | None = Field(default=None, description="Major/field of study, if stated separately from the degree name.")
    institution_name: str = Field(description="Name of the school/university/college.")
    location: str | None = Field(default=None, description="Institution location, if present.")
    start_date: str | None = Field(default=None, description="Start date as printed on the resume, if present.")
    end_date: str | None = Field(default=None, description="End/graduation date as printed on the resume, if present.")
    gpa: str | None = Field(default=None, description="GPA/percentage/grade, if stated. Kept as string since formats vary (e.g. '8.5/10', '3.9', 'First Class').")
    honors: list[str] = Field(default_factory=list, description="Honors, awards, or distinctions tied to this education entry (e.g. 'Dean's List', 'Cum Laude'), if listed.")


class Project(BaseModel):
    name: str = Field(description="Project name/title.")
    description: str | None = Field(default=None, description="Short description of what the project is/does.")
    technologies: list[str] = Field(default_factory=list, description="Technologies, languages, or tools used, if listed.")
    url: str | None = Field(default=None, description="Link to the project (repo, live demo, etc.), if present.")
    start_date: str | None = Field(default=None, description="Start date, if present.")
    end_date: str | None = Field(default=None, description="End date, if present.")


class Certification(BaseModel):
    name: str = Field(description="Certification/license name.")
    issuing_organization: str | None = Field(default=None, description="Organization that issued the certification, if stated.")
    issue_date: str | None = Field(default=None, description="Date issued, if present.")
    expiration_date: str | None = Field(default=None, description="Expiration date, if present.")
    credential_id: str | None = Field(default=None, description="Credential/license ID, if present.")


class Language(BaseModel):
    name: str = Field(description="Language name, e.g. 'Spanish'.")
    proficiency: str | None = Field(default=None, description="Stated proficiency level, e.g. 'Native', 'Fluent', 'Intermediate', if given.")

class Skills(BaseModel):
    category: str
    skills: list


class ResumeFields(ExtractedDocument):
    document_type: Literal["resume"] = "resume"

    full_name: str = Field(description="Candidate's full name.")
    headline: str | None = Field(default=None, description="Professional title/headline near the top of the resume, e.g. 'Senior Backend Engineer', if present.")
    summary: str | None = Field(default=None, description="Professional summary/objective paragraph, if present.")
    contact_info: ContactInfo = Field(default_factory=ContactInfo, description="Contact details extracted from the resume.")

    work_experience: list[WorkExperience] = Field(default_factory=list, description="Work history, ideally in the order listed on the resume (usually reverse-chronological).")
    education: list[Education] = Field(default_factory=list, description="Educational background.")
    skills: list[Skills] = Field(default_factory=list, description="skills as listed on the resume (technical and non-technical), keep grouped as given in the resume and even if not grouped on resume, for better representation group it.")
    projects: list[Project] = Field(default_factory=list, description="Personal/academic/professional projects listed separately from work experience.")
    certifications: list[Certification] = Field(default_factory=list, description="Certifications and licenses.")
    languages: list[Language] = Field(default_factory=list, description="Spoken/written languages, if listed.")

    total_years_experience: float | None = Field(default=None, description="Total years of experience, only if explicitly stated on the resume (e.g. in a summary line) — not calculated from work history dates.")

    # ====================== BUSINESS RULES ======================
    @model_validator(mode="after")
    def business_rules(self):
        errors = []

        # 1. Name must exist and be reasonable
        if not self.full_name or len(self.full_name.strip()) < 2:
            errors.append("Full name is missing or too short")

        # 2. At least one contact method
        contact = self.contact_info
        has_contact = any([
            contact.email,
            contact.phone,
            contact.linkedin_url,
            contact.github_url,
            contact.portfolio_url,
        ])
        if not has_contact:
            errors.append("At least one contact method (email, phone, LinkedIn, GitHub, or portfolio) is required")

        # 3. Basic email sanity check
        if contact.email and "@" not in contact.email:
            errors.append(f"Email looks invalid: {contact.email}")

        # 4. Basic phone sanity check (must contain several digits)
        # if contact.phone and not re.search(r"\d{7,}", contact.phone):
        #     errors.append(f"Phone number looks invalid: {contact.phone}")

        # 5. Work experience must have title + company
        for i, exp in enumerate(self.work_experience, 1):
            if not exp.job_title.strip():
                errors.append(f"Work experience #{i}: job title is missing")
            if not exp.company_name.strip():
                errors.append(f"Work experience #{i}: company name is missing")

        # 6. Education must have institution
        for i, edu in enumerate(self.education, 1):
            if not edu.institution_name.strip():
                errors.append(f"Education #{i}: institution name is missing")

        # 7. Resume should not be completely empty
        if (not self.work_experience 
            and not self.education 
            and not self.skills 
            and not self.projects):
            errors.append("Resume appears empty (no experience, education, skills or projects)")

        if errors:
            raise ValueError(" \n ".join(errors))

        return self