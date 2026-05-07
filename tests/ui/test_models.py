import pytest
from src.ui.models import Preset, CustomPreset, FavoritesManager
import json


def test_preset_creation():
    """Preset can be created and accessed"""
    preset = Preset(
        id=0,
        name="Waveform",
        theme="core",
        description="Classic oscillating waveform",
        shader="core/waveform",
        tags=["classic", "simple"],
        difficulty="easy"
    )
    assert preset.id == 0
    assert preset.name == "Waveform"
    assert preset.theme == "core"


def test_preset_to_dict():
    """Preset converts to dictionary"""
    preset = Preset(0, "Test", "core", "desc", "shader", [], "easy")
    data = preset.to_dict()
    assert data['id'] == 0
    assert data['name'] == "Test"
    assert isinstance(data, dict)


def test_custom_preset_creation():
    """CustomPreset can be created with parameters"""
    custom = CustomPreset(
        id="custom_001",
        name="My Neon",
        base_preset=45,
        parameters={"bass_sensitivity": 2.0}
    )
    assert custom.id == "custom_001"
    assert custom.parameters["bass_sensitivity"] == 2.0


def test_favorites_manager():
    """FavoritesManager tracks favorites"""
    mgr = FavoritesManager()
    mgr.add(5)
    mgr.add("custom_001")
    assert mgr.is_favorite(5)
    assert mgr.is_favorite("custom_001")
    assert not mgr.is_favorite(999)


def test_preset_from_dict():
    """Preset can be deserialized from dictionary"""
    data = {
        'id': 1,
        'name': 'Neon',
        'theme': 'cyberpunk',
        'description': 'Neon theme',
        'shader': 'neon/main',
        'tags': ['neon', 'bright'],
        'difficulty': 'medium'
    }
    preset = Preset.from_dict(data)
    assert preset.id == 1
    assert preset.name == 'Neon'
    assert preset.theme == 'cyberpunk'
    assert preset.tags == ['neon', 'bright']


def test_custom_preset_with_all_fields():
    """CustomPreset can be created with all optional fields"""
    custom = CustomPreset(
        id="custom_002",
        name="Mixed Preset",
        base_preset=10,
        parameters={"brightness": 1.5, "speed": 0.8},
        mix_preset=20
    )
    assert custom.id == "custom_002"
    assert custom.base_preset == 10
    assert custom.mix_preset == 20
    assert custom.parameters["brightness"] == 1.5
    assert custom.created is not None
    assert custom.modified is not None


def test_custom_preset_to_dict():
    """CustomPreset converts to dictionary with timestamps"""
    custom = CustomPreset(
        id="custom_003",
        name="Test Custom",
        base_preset=5,
        parameters={"param1": 1.0}
    )
    data = custom.to_dict()
    assert data['id'] == "custom_003"
    assert data['name'] == "Test Custom"
    assert data['base_preset'] == 5
    assert 'created' in data
    assert 'modified' in data


def test_custom_preset_from_dict():
    """CustomPreset can be deserialized from dictionary"""
    data = {
        'id': 'custom_004',
        'name': 'Loaded Custom',
        'base_preset': 15,
        'parameters': {'param1': 2.0, 'param2': 0.5},
        'mix_preset': 25,
        'created': '2026-05-07T12:00:00',
        'modified': '2026-05-07T13:00:00'
    }
    custom = CustomPreset.from_dict(data)
    assert custom.id == 'custom_004'
    assert custom.base_preset == 15
    assert custom.mix_preset == 25
    assert custom.parameters['param1'] == 2.0


def test_favorites_manager_toggle():
    """FavoritesManager toggle returns new state"""
    mgr = FavoritesManager()

    # Toggle on
    result = mgr.toggle(5)
    assert result is True
    assert mgr.is_favorite(5)

    # Toggle off
    result = mgr.toggle(5)
    assert result is False
    assert not mgr.is_favorite(5)


def test_favorites_manager_remove():
    """FavoritesManager can remove favorites"""
    mgr = FavoritesManager()
    mgr.add(10)
    assert mgr.is_favorite(10)

    mgr.remove(10)
    assert not mgr.is_favorite(10)


def test_favorites_manager_list_conversion():
    """FavoritesManager converts to and from list"""
    mgr = FavoritesManager()
    mgr.add(1)
    mgr.add(5)
    mgr.add("custom_001")

    favorites_list = mgr.to_list()
    assert len(favorites_list) == 3
    assert 1 in favorites_list
    assert 5 in favorites_list
    assert "custom_001" in favorites_list

    # Test from_list
    mgr2 = FavoritesManager()
    mgr2.from_list(favorites_list)
    assert mgr2.is_favorite(1)
    assert mgr2.is_favorite(5)
    assert mgr2.is_favorite("custom_001")


def test_preset_from_dict_missing_required_field():
    """Preset.from_dict raises ValueError when required fields are missing"""
    # Missing 'id' field
    data_missing_id = {
        'name': 'Neon',
        'theme': 'cyberpunk',
        'description': 'Neon theme',
        'shader': 'neon/main'
    }
    with pytest.raises(ValueError, match="Missing required field"):
        Preset.from_dict(data_missing_id)

    # Missing 'shader' field
    data_missing_shader = {
        'id': 1,
        'name': 'Neon',
        'theme': 'cyberpunk',
        'description': 'Neon theme'
    }
    with pytest.raises(ValueError, match="Missing required field"):
        Preset.from_dict(data_missing_shader)


def test_custom_preset_from_dict_missing_required_field():
    """CustomPreset.from_dict raises ValueError when required fields are missing"""
    # Missing 'base_preset' field
    data_missing_base = {
        'id': 'custom_001',
        'name': 'My Preset',
        'parameters': {}
    }
    with pytest.raises(ValueError, match="Missing required field"):
        CustomPreset.from_dict(data_missing_base)

    # Missing 'name' field
    data_missing_name = {
        'id': 'custom_001',
        'base_preset': 5
    }
    with pytest.raises(ValueError, match="Missing required field"):
        CustomPreset.from_dict(data_missing_name)


def test_custom_preset_timestamp_auto_generation():
    """CustomPreset auto-generates timestamps"""
    custom = CustomPreset(
        id="custom_auto",
        name="Auto Timestamp",
        base_preset=1,
        parameters={}
    )
    assert custom.created is not None
    assert custom.modified is not None
    # Timestamps should be ISO format strings
    assert isinstance(custom.created, str)
    assert isinstance(custom.modified, str)
    assert 'T' in custom.created
    assert 'T' in custom.modified


def test_custom_preset_empty_parameters():
    """CustomPreset can have empty parameters dict"""
    custom = CustomPreset(
        id="custom_empty",
        name="Empty Params",
        base_preset=5
    )
    assert custom.parameters == {}
    data = custom.to_dict()
    assert data['parameters'] == {}


def test_custom_preset_from_dict_empty_parameters():
    """CustomPreset.from_dict handles missing parameters field"""
    data = {
        'id': 'custom_005',
        'name': 'No Params',
        'base_preset': 10
    }
    custom = CustomPreset.from_dict(data)
    assert custom.parameters == {}


def test_favorites_manager_toggle_multiple_times():
    """FavoritesManager toggle works correctly with multiple toggles"""
    mgr = FavoritesManager()
    preset_id = 42

    # Toggle on
    assert mgr.toggle(preset_id) is True
    assert mgr.is_favorite(preset_id)

    # Toggle off
    assert mgr.toggle(preset_id) is False
    assert not mgr.is_favorite(preset_id)

    # Toggle on again
    assert mgr.toggle(preset_id) is True
    assert mgr.is_favorite(preset_id)

    # Toggle off again
    assert mgr.toggle(preset_id) is False
    assert not mgr.is_favorite(preset_id)


def test_favorites_manager_empty_list_conversion():
    """FavoritesManager handles empty list conversion"""
    mgr = FavoritesManager()
    empty_list = mgr.to_list()
    assert empty_list == []

    mgr2 = FavoritesManager()
    mgr2.from_list([])
    assert mgr2.to_list() == []


def test_preset_to_dict_type():
    """Preset.to_dict returns Dict[str, Any]"""
    preset = Preset(0, "Test", "core", "desc", "shader")
    data = preset.to_dict()
    assert isinstance(data, dict)
    assert all(isinstance(k, str) for k in data.keys())


def test_custom_preset_to_dict_type():
    """CustomPreset.to_dict returns Dict[str, Any]"""
    custom = CustomPreset(
        id="custom_006",
        name="Type Test",
        base_preset=1
    )
    data = custom.to_dict()
    assert isinstance(data, dict)
    assert all(isinstance(k, str) for k in data.keys())
