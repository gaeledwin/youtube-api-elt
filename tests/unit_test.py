import pytest
from unittest.mock import MagicMock, patch
from datetime import time, timedelta

# Import des fonctions à tester
import sys
sys.path.insert(0, './dags')  # pour que Python trouve tes modules
from data_warehouse.data_transformation import parse_duration, transform_data
from data_warehouse.data_load import load_data
from data_warehouse.data_modification import insert_row, update_row, delete_row


def test_parse_duration_minutes_second():
    result = parse_duration("PT10M30S")
    assert result == timedelta(minutes=10, seconds=30)
    
def test_parse_duration_second():
    result = parse_duration('PT50S')
    assert result == timedelta(seconds=50)

def test_parse_duration_minutes():
    result = parse_duration("PT45M")
    assert result == timedelta(minutes=45)

def test_parse_duration_all():
    result = parse_duration("PT2D3H45M26S")
    assert result == timedelta(days=2, hours=3, minutes=45, seconds=26)
    
def test_row_type_normal(sample_video_row_core):
    result = transform_data(sample_video_row_core)
    assert result['Type'] == "Normal"

def test_row_type_shorts(short_video_row):
    result = transform_data(short_video_row)
    assert result["Type"] == "Shorts"