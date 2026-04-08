from app.config import settings


def _fallback_triage(text: str) -> dict:
    lower = text.lower()

    if any(k in lower for k in ["ransomware", "domain admin", "exfiltration", "c2"]):
        severity = "Critical"
        threat_type = "Malware / Intrusion"
    elif any(k in lower for k in ["impossible travel", "malware", "phishing", "password spray", "failed login"]):
        severity = "High"
        threat_type = "Identity / Endpoint"
    elif any(k in lower for k in ["suspicious", "unusual", "new device"]):
        severity = "Medium"
        threat_type = "Anomaly"
    else:
        severity = "Low"
        threat_type = "Informational"

    return {
        "severity": severity,
        "summary": f"Local triage fallback classified the event as {severity}.",
        "recommendation": "Review supporting logs, validate scope, and escalate if malicious activity is confirmed.",
        "threat_type": threat_type,
        "provider": "local-fallback",
    }


def triage_alert(text: str) -> dict:
    if not settings.openai_api_key:
        return _fallback_triage(text)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        prompt = f'''
You are a cybersecurity SOC analyst assistant.
Return a JSON object with keys:
severity, summary, recommendation, threat_type, provider

Alert:
{text}
'''
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are a concise cybersecurity triage assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        content = response.choices[0].message.content or ""
        # Minimal tolerant parsing
        import json
        data = json.loads(content)
        data["provider"] = "openai"
        return data
    except Exception:
        return _fallback_triage(text)
