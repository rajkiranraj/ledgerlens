import json
import time
import logging
import requests
from typing import Dict, List, Any
from django.conf import settings

logger = logging.getLogger(__name__)


def build_insights_prompt(data: Dict[str, Any]) -> str:
    """Build prompt for expense insights generation"""
    return f"""You are a financial data analyst. Rules:
1. Never invent statistics or values
2. Only use data provided
3. Keep outputs concise
4. Return valid JSON only
5. No markdown or extra explanations
6. Max 5 insights total
7. Use business-oriented language

Input data:
{json.dumps(data, indent=2)}

Respond strictly with JSON in this format:
{{"summary": "1-2 sentence executive summary", "insights": ["insight 1", "insight 2", ...]}}"""


def build_import_summary_prompt(data: Dict[str, Any]) -> str:
    """Build prompt for import summary generation"""
    return f"""You are a financial data analyst. Rules:
1. Never invent statistics or values
2. Only use data provided
3. Keep output 100-150 words
4. Return valid JSON only
5. No markdown or extra explanations
6. Use business-readable language
7. Rate data quality as Poor/Fair/Good/Excellent based on anomaly rate

Input data:
{json.dumps(data, indent=2)}

Respond strictly with JSON in this format:
{{"summary": "executive import summary"}}"""


def generate_deterministic_insights(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate insights using deterministic rules when AI is unavailable"""
    insights = []
    summary = "Expense analysis summary."

    total_expenses = data.get("total_expenses", 0)
    spending_by_category = data.get("spending_by_category", {})

    # Rule 1: Check travel spending >30%
    if "Travel" in spending_by_category and total_expenses > 0:
        travel_share = (spending_by_category["Travel"] / total_expenses) * 100
        if travel_share > 30:
            insights.append(f"Travel represents {round(travel_share)}% of total spending.")

    # Rule 2: Check elevated anomaly rate
    anomaly_rate = data.get("anomaly_rate", 0)
    if anomaly_rate > 10:
        insights.append(f"Elevated anomaly rate detected ({round(anomaly_rate)}%).")

    # Rule 3: Check significant growth
    monthly_growth = data.get("monthly_growth", 0)
    if monthly_growth > 20:
        insights.append(f"Significant spending increase observed ({round(monthly_growth)}% month-over-month).")

    # Rule 4: Check top category concentration
    if spending_by_category:
        top_category = max(spending_by_category.items(), key=lambda x: x[1])
        top_share = (top_category[1] / total_expenses) * 100 if total_expenses > 0 else 0
        if top_share > 25:
            insights.append(f"{top_category[0]} is the largest expense category ({round(top_share)}%).")

    # Rule 5: Check import activity
    import_count = data.get("total_imports", 0)
    if import_count > 5:
        insights.append(f"Active import history with {import_count} imports.")

    # Ensure max 5 insights
    insights = insights[:5]

    if not insights:
        insights = ["Expense data available for analysis."]

    return {
        "summary": summary,
        "insights": insights
    }


def generate_deterministic_import_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate import summary using deterministic rules when AI is unavailable"""
    total_rows = data.get("total_rows", 0)
    imported = data.get("imported_rows", 0)
    rejected = data.get("rejected_rows", 0)
    corrected = data.get("corrected_rows", 0)

    intervention = rejected + corrected
    success_rate = (imported / total_rows) * 100 if total_rows > 0 else 100

    if success_rate >= 95:
        quality = "Excellent"
    elif success_rate >= 80:
        quality = "Good"
    elif success_rate >= 60:
        quality = "Fair"
    else:
        quality = "Poor"

    summary = (
        f"Import completed successfully. {imported} records were imported. "
        f"{intervention} records required intervention. "
        f"Data quality was rated {quality}."
    )
    return {"summary": summary}


def call_spreetail_ai_api(prompt: str) -> str:
    """Call Spreetail AI (NVIDIA NIM backend) with timeout handling"""
    if not settings.AI_ENABLED:
        raise Exception("AI is disabled")

    try:
        headers = {
            "Authorization": f"Bearer {settings.SPREETAIL_AI_API_KEY}",
            "Accept": "application/json"
        }

        payload = {
            "model": settings.SPREETAIL_AI_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
            "temperature": 0.20,
            "top_p": 0.70,
            "frequency_penalty": 0.00,
            "presence_penalty": 0.00,
            "stream": False
        }

        response = requests.post(
            settings.SPREETAIL_AI_INVOKE_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()
        response_data = response.json()

        # Extract the assistant's message
        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"]
        else:
            raise Exception("Invalid response format from Spreetail AI")

    except requests.exceptions.RequestException as e:
        logger.error(f"Spreetail AI API call failed: {e}")
        raise


def parse_ai_response(response_text: str) -> Dict[str, Any]:
    """Parse and validate AI JSON response"""
    try:
        # Clean up response (remove any extra characters)
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        data = json.loads(cleaned.strip())
        return data
    except Exception as e:
        logger.error(f"Failed to parse AI response: {e}")
        raise


def get_cached_result(cache_key: str) -> Any:
    """Get cached AI result with TTL check"""
    if cache_key in settings.AI_CACHE:
        cached_data, timestamp = settings.AI_CACHE[cache_key]
        if time.time() - timestamp < settings.AI_CACHE_TTL:
            return cached_data
        else:
            del settings.AI_CACHE[cache_key]
    return None


def set_cached_result(cache_key: str, data: Any) -> None:
    """Cache AI result"""
    settings.AI_CACHE[cache_key] = (data, time.time())


def clear_group_cache(group_id: int) -> None:
    """Clear all cached data for a group (called when data changes)"""
    keys_to_delete = [k for k in settings.AI_CACHE if k.startswith(f"{group_id}_")]
    for key in keys_to_delete:
        del settings.AI_CACHE[key]
    logger.info(f"Cleared AI cache for group {group_id}")
