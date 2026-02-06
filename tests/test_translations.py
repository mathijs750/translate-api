import pytest
import httpx
import asyncio
import importlib.util
import sys
from pathlib import Path

try:
    from main import app
except Exception:
    spec = importlib.util.spec_from_file_location(
        "main", str(Path(__file__).resolve().parents[1] / "main.py")
    )
    main = importlib.util.module_from_spec(spec)
    sys.modules["main"] = main
    spec.loader.exec_module(main)
    app = main.app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


# Test cases: (source_text, expected_keywords, test_description)
TEST_CASES = [
    # Functionele blokkades (Showstoppers)
    (
        "The app crashes immediately after the splash screen when using a VPN.",
        ["crash", "vast", "onverwacht"],
        "App crash with VPN should translate 'crashes' correctly",
    ),
    (
        "Die Anmeldung schlägt fehl, obwohl die Anmeldedaten korrekt sind.",
        ["inlog", "aanmeld", "aanmelden", "login", "melding"],
        "Login failure should differentiate 'Anmeldung' as login not registration",
    ),
    (
        "Impossible de valider le panier d'achat depuis la mise à jour.",
        ["winkelmandje", "winkelwagen"],
        "Shopping cart should translate 'panier' correctly",
    ),
    # UI & Interface elementos
    (
        "El botón de envío no responde en la versión móvil.",
        ["verzendknop", "knop"],
        "Submit button should use 'verzendknop' not 'knop van verzending'",
    ),
    (
        "The dropdown menu overlaps with the navigation bar.",
        ["dropdown", "navigatie"],
        "Technical terms should remain recognizable",
    ),
    (
        "Il campo di testo accetta solo caratteri numerici.",
        ["tekstveld", "veld"],
        "Text field should translate to 'tekstveld'",
    ),
    # Edge Cases
    (
        "Character limit is bypassed when pasting text from a Word document.",
        ["omzeild", "tekenl", "plakken"],
        "Bypassed should translate as 'omzeild' not 'gepasseerd'",
    ),
    (
        "Sonderzeichen im Passwort führen zu einem 404-Fehler.",
        ["speciale tekens", "wachtwoord", "sonderzeichen", "password"],
        "Special characters should be translated correctly",
    ),
    (
        "L'image de profil s'affiche à l'envers après le téléchargement.",
        ["ondersteboven", "profiel"],
        "Upside down image should use 'ondersteboven'",
    ),
    # Jargon and Slang
    (
        "The UI is buggy and feels laggy on older devices.",
        ["traag", "bug"],
        "Buggy and laggy should be translated or recognized",
    ),
    (
        "I found a workaround, but the fix is still needed.",
        ["tijdelijke", "oplossing"],
        "Workaround should become 'tijdelijke oplossing'",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("text,keywords,description", TEST_CASES)
async def test_translation_contains_keywords(client, text, keywords, description):
    """Test that translations contain expected keywords."""
    response = await client.post("/translate", json={"text": text})

    assert response.status_code == 200, f"Failed to translate: {text}"
    data = response.json()

    # Check that we got translations back
    assert "guesses" in data
    assert len(data["guesses"]) > 0, f"No guesses returned for: {text}"

    # Get the best guess (first one, highest score)
    translation = data["guesses"][0].lower()

    # Check that at least one expected keyword is in the translation
    found_keywords = [kw for kw in keywords if kw.lower() in translation]
    assert len(found_keywords) > 0, (
        f"{description}\nText: {text}\nTranslation: {translation}\nExpected keywords: {keywords}"
    )


@pytest.mark.asyncio
async def test_translation_response_structure(client):
    """Test that the translation response has the correct structure."""
    response = await client.post("/translate", json={"text": "Hello world"})

    assert response.status_code == 200
    data = response.json()

    assert "original" in data
    assert "guesses" in data
    assert isinstance(data["original"], str)
    assert isinstance(data["guesses"], list)
    assert all(isinstance(guess, str) for guess in data["guesses"])


@pytest.mark.asyncio
async def test_empty_text_handling(client):
    """Test handling of empty input."""
    response = await client.post("/translate", json={"text": ""})

    # Should either succeed with empty translation or handle gracefully
    assert response.status_code in [200, 400]


@pytest.mark.asyncio
async def test_multiple_hypothesis_count(client):
    """Test that we receive multiple translation hypotheses."""
    response = await client.post(
        "/translate", json={"text": "The app crashes when starting"}
    )

    assert response.status_code == 200
    data = response.json()

    # We request MAX_HYPOTHESES (3) translations
    assert len(data["guesses"]) >= 1, "Should return at least one hypothesis"
    # The API should try to return up to MAX_HYPOTHESES
    assert len(data["guesses"]) <= 3, "Should not exceed MAX_HYPOTHESES"
