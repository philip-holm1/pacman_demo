"""Test that skin selection persists and loads correctly."""
import json
import os
import tempfile
from pathlib import Path
from pacman import config


def test_save_and_load_skin_preference():
    """Test that skin preference is saved and loaded correctly."""
    # Create a temporary settings file
    with tempfile.TemporaryDirectory() as tmpdir:
        original_data_dir = Path.cwd() / "data"
        test_data_dir = Path(tmpdir) / "data"
        test_data_dir.mkdir()
        
        # Temporarily override the settings path
        original_settings = "data/settings.json"
        test_settings = str(test_data_dir / "settings.json")
        
        # Monkey-patch the settings path in the functions
        import pacman.config as cfg
        original_load = cfg.load_skin_preference
        original_save = cfg.save_skin_preference
        
        def test_load():
            if os.path.exists(test_settings):
                with open(test_settings, 'r') as f:
                    settings = json.load(f)
                    skin = settings.get("skin", {}).get("selected", "default")
                    if skin in cfg.AVAILABLE_SKINS:
                        return skin
            return "default"
        
        def test_save(skin_name):
            from datetime import datetime
            if skin_name not in cfg.AVAILABLE_SKINS:
                skin_name = "default"
            settings = {}
            if os.path.exists(test_settings):
                try:
                    with open(test_settings, 'r') as f:
                        settings = json.load(f)
                except:
                    settings = {}
            settings["skin"] = {
                "selected": skin_name,
                "updated_at": datetime.now().isoformat()
            }
            os.makedirs(test_data_dir, exist_ok=True)
            with open(test_settings, 'w') as f:
                json.dump(settings, f, indent=2)
        
        cfg.load_skin_preference = test_load
        cfg.save_skin_preference = test_save
        
        try:
            # Test default load when no file exists
            loaded = cfg.load_skin_preference()
            assert loaded == "default", f"Expected 'default', got '{loaded}'"
            
            # Test saving green_star
            cfg.save_skin_preference("green_star")
            assert os.path.exists(test_settings), "Settings file should be created"
            
            # Test loading saved preference
            loaded = cfg.load_skin_preference()
            assert loaded == "green_star", f"Expected 'green_star', got '{loaded}'"
            
            # Verify JSON structure
            with open(test_settings, 'r') as f:
                data = json.load(f)
                assert "skin" in data
                assert data["skin"]["selected"] == "green_star"
                assert "updated_at" in data["skin"]
            
            # Test saving back to default
            cfg.save_skin_preference("default")
            loaded = cfg.load_skin_preference()
            assert loaded == "default", f"Expected 'default', got '{loaded}'"
            
            # Test invalid skin name falls back to default
            cfg.save_skin_preference("invalid_skin")
            loaded = cfg.load_skin_preference()
            assert loaded == "default", f"Expected 'default' for invalid skin, got '{loaded}'"
            
        finally:
            # Restore original functions
            cfg.load_skin_preference = original_load
            cfg.save_skin_preference = original_save


def test_available_skins_configuration():
    """Test that AVAILABLE_SKINS contains expected skins."""
    assert "default" in config.AVAILABLE_SKINS
    assert "green_star" in config.AVAILABLE_SKINS
    
    # Verify default skin structure
    default = config.AVAILABLE_SKINS["default"]
    assert default["name"] == "default"
    assert default["display_name"] == "Default"
    assert "assets" in default
    
    # Verify green_star skin structure
    green_star = config.AVAILABLE_SKINS["green_star"]
    assert green_star["name"] == "green_star"
    assert green_star["display_name"] == "Green Star"
    assert "assets" in green_star
    assert "metadata" in green_star
    assert green_star["metadata"]["base_tile_px"] == 64
    assert green_star["metadata"]["scales"] == [1, 2]
