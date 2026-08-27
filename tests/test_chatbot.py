import pytest
from app import (
    calculate_bmi,
    calculate_bmr,
    calculate_water_intake,
    calculate_heart_rate_zones,
    SYSTEM_INSTRUCTIONS
)
from Healthcarechatbot import SYSTEM_INSTRUCTION as CLI_SYSTEM_INSTRUCTION

def test_calculate_bmi():
    # Test Normal Weight
    score, cat, color = calculate_bmi(70, 175)
    assert score == 22.9
    assert cat == "Normal Weight"

    # Test Underweight
    score, cat, _ = calculate_bmi(45, 170)
    assert cat == "Underweight"

    # Test Overweight
    score, cat, _ = calculate_bmi(85, 175)
    assert cat == "Overweight"

    # Test Obesity
    score, cat, _ = calculate_bmi(110, 170)
    assert cat == "Obesity"

    # Test Edge Cases
    score, cat, _ = calculate_bmi(0, 170)
    assert cat == "Invalid Input"

def test_calculate_bmr():
    # Test Male
    bmr_m, tdee_m = calculate_bmr(70, 175, 25, "Male", "Moderately Active (3-5 days/week)")
    assert bmr_m > 1600
    assert tdee_m > bmr_m

    # Test Female
    bmr_f, tdee_f = calculate_bmr(60, 165, 30, "Female", "Sedentary (Little/no exercise)")
    assert bmr_f > 1200
    assert tdee_f == round(bmr_f * 1.2)

    # Invalid input
    assert calculate_bmr(0, 170, 25, "Male", "Sedentary") == (0, 0)

def test_calculate_water_intake():
    # Base calculation
    water_base = calculate_water_intake(70, 0, False)
    assert water_base == round(70 * 0.033, 2)

    # With exercise and hot weather
    water_active = calculate_water_intake(70, 60, True)
    assert water_active > water_base

def test_calculate_heart_rate_zones():
    zones = calculate_heart_rate_zones(30, 70)
    assert "Warm-up (50-60%)" in zones
    assert "Peak (90-100%)" in zones
    # Max heart rate for 30 yo is 190. Peak max should be 190
    assert zones["Peak (90-100%)"][1] == 190

def test_system_instructions_contain_disclaimers():
    assert "safety disclaimer" in CLI_SYSTEM_INSTRUCTION.lower() or "disclaimer" in CLI_SYSTEM_INSTRUCTION.lower()
    for mode, prompt in SYSTEM_INSTRUCTIONS.items():
        assert "disclaimer" in prompt.lower() or "triage" in prompt.lower() or "guidance" in prompt.lower()
