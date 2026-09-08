# tests/conftest.py
import pytest

# Une "fixture" = un objet prêt à l'emploi pour tes tests
# @pytest.fixture dit à pytest : "cette fonction crée un objet réutilisable"

@pytest.fixture
def sample_video_row_staging():
    """Simule une ligne de données venant de l'API YouTube (format staging)"""
    return {
        "video_id": "abc123",
        "title": "Mon super tutoriel Python",
        "publishedAt": "2024-01-15T10:00:00Z",
        "duration": "PT10M30S",
        "viewCount": 1500,
        "likeCount": 80,
        "commentCount": 12
    }
    

@pytest.fixture
def sample_video_row_core():
    """Simule une ligne de données dans le schéma core (après transformation)"""
    return {
        "Video_Id": "abc123",
        "Video_Title": "Mon super tutoriel Python",
        "Uploads_Date": "2024-01-15T10:00:00Z",
        "Duration": "PT10M30S",
        "View_Count": 1500,
        "Like_Count": 80,
        "Comment_Count": 12
    }

@pytest.fixture
def short_video_row():
    """Une vidéo Shorts (durée <= 60 secondes)"""
    return {
        "Video_Id": "xyz789",
        "Video_Title": "Short vidéo",
        "Uploads_Date": "2024-03-01T08:00:00Z",
        "Duration": "PT45S",
        "View_Count": 500,
        "Like_Count": 20,
        "Comment_Count": 2
    }