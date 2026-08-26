from pydantic import BaseModel, Field
from typing import Literal

from app.schemas.base_schema import ExtractedDocument


class Address(BaseModel):
    street: str | None = Field(
        default=None,
        description="Street address, including building, apartment, building, or suite number, if present."
    )
    city: str | None = Field(
        default=None,
        description="City."
    )
    state: str | None = Field(
        default=None,
        description="State or province."
    )
    postal_code: str | None = Field(
        default=None,
        description="Postal or ZIP code."
    )
    country: str | None = Field(
        default=None,
        description="Country."
    )


class ContactInfo(BaseModel):
    """Applicant's contact information."""

    phone: str | None = Field(
        default=None,
        description="Applicant's phone number, if present."
    )
    email: str | None = Field(
        default=None,
        description="Applicant's email address, if present."
    )
    address: Address | None = Field(
        default=None,
        description="Applicant's residential or mailing address, if present."
    )


class PersonalInfo(BaseModel):
    """Basic identifying information about the applicant."""

    first_name: str | None = Field(
        default=None,
        description="Applicant's first/given name."
    )
    middle_name: str | None = Field(
        default=None,
        description="Applicant's middle name, if present."
    )
    last_name: str | None = Field(
        default=None,
        description="Applicant's last/family name."
    )
    full_name: str = Field(
        description="Applicant's complete name as printed on the application."
    )
    date_of_birth: str | None = Field(
        default=None,
        description="Applicant's date of birth, in DD-MM-YYYY format, if present."
    )
    nationality: str | None = Field(
        default=None,
        description="Applicant's nationality, if present."
    )
    gender: str | None = Field(
        default=None,
        description="Applicant's gender as stated on the application, if present."
    )


class EducationEntry(BaseModel):
    """One educational qualification or academic record."""

    institution_name: str = Field(
        description="Name of the school, college, university, or educational institution."
    )
    degree_or_qualification: str | None = Field(
        default=None,
        description="Degree, diploma, certification, or qualification obtained or pursued."
    )
    field_of_study: str | None = Field(
        default=None,
        description="Major, specialization, stream, or field of study."
    )
    start_date: str | None = Field(
        default=None,
        description="Start date of the education period, if present."
    )
    end_date: str | None = Field(
        default=None,
        description="End or graduation date, if present."
    )
    grade_or_score: str | None = Field(
        default=None,
        description="Grade, percentage, GPA, CGPA, or other academic score, if present."
    )


class EmploymentEntry(BaseModel):
    """One previous or current employment record."""

    employer_name: str = Field(
        description="Name of the employer or organization."
    )
    job_title: str | None = Field(
        default=None,
        description="Job title or position held."
    )
    start_date: str | None = Field(
        default=None,
        description="Employment start date, if present."
    )
    end_date: str | None = Field(
        default=None,
        description="Employment end date, if present. Null if currently employed or not stated."
    )
    responsibilities: str | None = Field(
        default=None,
        description="Description of responsibilities or duties, if present."
    )


class Reference(BaseModel):
    """Professional, academic, or personal reference."""

    name: str = Field(
        description="Reference person's name."
    )
    relationship: str | None = Field(
        default=None,
        description="Relationship of the reference to the applicant, e.g. manager, professor, colleague."
    )
    organization: str | None = Field(
        default=None,
        description="Reference person's organization or institution, if present."
    )
    phone: str | None = Field(
        default=None,
        description="Reference person's phone number, if present."
    )
    email: str | None = Field(
        default=None,
        description="Reference person's email address, if present."
    )


class ApplicationFormFields(ExtractedDocument):

    document_type: Literal["application_form"] = "application_form"

    application_number: str | None = Field(
        default=None,
        description="Application, registration, or reference number assigned to the application, if present."
    )
    application_date: str | None = Field(
        default=None,
        description="Date the application was submitted or completed, in DD-MM-YYYY format, if present."
    )
    application_type: str | None = Field(
        default=None,
        description="Type or category of application, if stated."
    )

    personal_info: PersonalInfo = Field(
        description="Basic personal information of the applicant."
    )

    contact_info: ContactInfo = Field(
        description="Applicant's contact information."
    )

    education: list[EducationEntry] = Field(
        default_factory=list,
        description="Applicant's educational qualifications or academic history."
    )

    employment_history: list[EmploymentEntry] = Field(
        default_factory=list,
        description="Applicant's previous or current employment history."
    )

    position_or_program: str | None = Field(
        default=None,
        description="Position, course, program, department, or opportunity the applicant is applying for."
    )
    preferred_location: str | None = Field(
        default=None,
        description="Preferred location or campus, if specified."
    )
    start_date_preference: str | None = Field(
        default=None,
        description="Preferred or available start date, if present."
    )

    skills: list[str] = Field(
        default_factory=list,
        description="Skills, competencies, or areas of expertise explicitly listed by the applicant."
    )
    certifications: list[str] = Field(
        default_factory=list,
        description="Professional or academic certifications listed by the applicant."
    )
    languages: list[str] = Field(
        default_factory=list,
        description="Languages known or spoken by the applicant, if listed."
    )

    references: list[Reference] = Field(
        default_factory=list,
        description="References provided by the applicant."
    )

    additional_information: str | None = Field(
        default=None,
        description="Additional information, comments, statements, or explanations provided by the applicant."
    )
    declaration: str | None = Field(
        default=None,
        description="Declaration or statement made by the applicant, if present."
    )
    signature_present: bool | None = Field(
        default=None,
        description="Whether an applicant signature is visibly present on the form."
    )