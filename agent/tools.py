"""Strands tool bound to a gate; receives original evidence before any LLM call."""

from strands import tool

from .decision import LeadGate


def make_qualify_tool(gate: LeadGate):
    @tool
    def qualify_lead(lead: dict) -> dict:
        """Gate original inbound founder or recruiter evidence for GTM outreach."""
        return gate.qualify(lead)

    return qualify_lead
