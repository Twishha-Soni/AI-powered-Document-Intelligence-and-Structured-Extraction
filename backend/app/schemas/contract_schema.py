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


class Party(BaseModel):
    """A party involved in the contract."""

    name: str = Field(
        description="Legal name of the individual or organization that is a party to the contract."
    )
    party_type: str | None = Field(
        default=None,
        description="Role of the party in the contract, e.g. buyer, seller, client, vendor, employer, employee, landlord, tenant."
    )
    address: Address | None = Field(
        default=None,
        description="Address of the party, if present."
    )
    contact_person: str | None = Field(
        default=None,
        description="Named representative or contact person for the party, if present."
    )
    email: str | None = Field(
        default=None,
        description="Contact email address, if present."
    )
    phone: str | None = Field(
        default=None,
        description="Contact phone number, if present."
    )


class PaymentTerm(BaseModel):
    """Payment terms specified in the contract."""

    description: str = Field(
        description="Description of the payment obligation or payment term."
    )
    amount: float | None = Field(
        default=None,
        ge=0,
        description="Payment amount, if explicitly stated."
    )
    currency: str | None = Field(
        default=None,
        description="ISO currency code, e.g. USD, INR, EUR, if applicable."
    )
    frequency: str | None = Field(
        default=None,
        description="Payment frequency, e.g. one-time, monthly, quarterly, annually, milestone-based."
    )
    due_date_or_terms: str | None = Field(
        default=None,
        description="Payment due date or terms, e.g. Net 30, within 15 days of invoice."
    )


class ContractClause(BaseModel):
    """A significant clause extracted from the contract."""

    clause_type: str = Field(
        description="Type of clause, e.g. confidentiality, termination, liability, indemnification, non-compete, intellectual_property, dispute_resolution."
    )
    title: str | None = Field(
        default=None,
        description="Title or heading of the clause, if present."
    )
    summary: str = Field(
        description="Concise summary of the substantive requirements or rights defined by the clause."
    )


class ContractFields(ExtractedDocument):

    document_type: Literal["contract"] = "contract"

    contract_title: str | None = Field(
        default=None,
        description="Title or name of the contract as printed in the document."
    )
    contract_number: str | None = Field(
        default=None,
        description="Contract or agreement identification number, if present."
    )
    contract_type: str | None = Field(
        default=None,
        description="Type of contract, e.g. employment, service agreement, lease, sales agreement, NDA, vendor agreement."
    )

    effective_date: str | None = Field(
        default=None,
        description="Date on which the contract becomes effective, in DD-MM-YYYY format, if present."
    )
    execution_date: str | None = Field(
        default=None,
        description="Date on which the contract was signed or executed, in DD-MM-YYYY format, if present."
    )

    parties: list[Party] = Field(
        min_length=1,
        description="Individuals or organizations that are parties to the contract."
    )

    start_date: str | None = Field(
        default=None,
        description="Start date of the contractual term, in DD-MM-YYYY format, if present."
    )
    end_date: str | None = Field(
        default=None,
        description="End date of the contractual term, in DD-MM-YYYY format, if present."
    )
    duration: str | None = Field(
        default=None,
        description="Contract duration as explicitly stated, e.g. 12 months, 2 years."
    )
    auto_renewal: bool | None = Field(
        default=None,
        description="Whether the contract automatically renews after the initial term, if stated."
    )
    renewal_terms: str | None = Field(
        default=None,
        description="Terms governing renewal or extension of the contract, if present."
    )

    purpose: str | None = Field(
        default=None,
        description="Purpose or primary objective of the contract."
    )
    scope_of_work: str | None = Field(
        default=None,
        description="Description of goods, services, work, or responsibilities covered by the contract."
    )
    obligations: list[str] = Field(
        default_factory=list,
        description="Key obligations or responsibilities explicitly assigned to the parties."
    )

    payment_terms: list[PaymentTerm] = Field(
        default_factory=list,
        description="Payment amounts and payment conditions specified in the contract."
    )
    total_contract_value: float | None = Field(
        default=None,
        ge=0,
        description="Total contract value, if explicitly stated."
    )
    currency: str | None = Field(
        default=None,
        description="ISO currency code for monetary amounts, e.g. USD, INR, EUR."
    )

    termination_notice_period: str | None = Field(
        default=None,
        description="Notice period required for termination, e.g. 30 days, 90 days."
    )
    termination_conditions: str | None = Field(
        default=None,
        description="Conditions or circumstances under which the contract may be terminated."
    )
    termination_penalty: str | None = Field(
        default=None,
        description="Penalty, fee, or financial consequence associated with termination, if stated."
    )

    governing_law: str | None = Field(
        default=None,
        description="Jurisdiction or governing law specified by the contract."
    )
    jurisdiction: str | None = Field(
        default=None,
        description="Court, location, or legal jurisdiction specified for disputes, if present."
    )
    dispute_resolution: str | None = Field(
        default=None,
        description="Method for resolving disputes, e.g. arbitration, mediation, litigation."
    )

    confidentiality: str | None = Field(
        default=None,
        description="Summary of confidentiality or non-disclosure obligations, if present."
    )
    intellectual_property: str | None = Field(
        default=None,
        description="Summary of intellectual property ownership, licensing, or usage rights, if present."
    )
    liability: str | None = Field(
        default=None,
        description="Summary of liability limitations or liability obligations, if present."
    )
    indemnification: str | None = Field(
        default=None,
        description="Summary of indemnification obligations, if present."
    )
    non_compete: str | None = Field(
        default=None,
        description="Summary of non-compete restrictions, if present."
    )
    non_solicitation: str | None = Field(
        default=None,
        description="Summary of non-solicitation restrictions, if present."
    )
    force_majeure: str | None = Field(
        default=None,
        description="Summary of force majeure provisions, if present."
    )

    clauses: list[ContractClause] = Field(
        default_factory=list,
        description="Other significant contract clauses not represented by the dedicated fields above."
    )

    signatures_present: bool | None = Field(
        default=None,
        description="Whether signatures are visibly present in the document."
    )
    signed_by: list[str] = Field(
        default_factory=list,
        description="Names of individuals who signed the contract, if identifiable."
    )

    amendments: list[str] = Field(
        default_factory=list,
        description="Amendments, addendums, or modifications referenced in the contract, if present."
    )
    notes: str | None = Field(
        default=None,
        description="Other relevant information explicitly stated in the contract."
    )