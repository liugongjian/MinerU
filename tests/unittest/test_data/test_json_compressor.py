import pytest
import json
from magic_pdf.libs.json_compressor import JsonCompressor

# Test data fixtures
@pytest.fixture
def test_cases():
    return [
        # Simple dictionary
        {"name": "John", "age": 30},
        
        # Nested dictionary
        {
            "person": {
                "name": "Alice",
                "address": {
                    "street": "123 Main St",
                    "city": "New York"
                }
            }
        },
        
        # List of dictionaries
        [
            {"id": 1, "value": "first"},
            {"id": 2, "value": "second"}
        ],
        
        # Dictionary with various data types
        {
            "string": "hello",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "array": [1, 2, 3],
            "nested": {"key": "value"}
        },
        
        # Empty structures
        {},
        [],
        {"empty_list": [], "empty_dict": {}}
    ]

@pytest.fixture
def large_data():
    return {
        "data": ["test" * 100] * 100  # Create a large repeated string
    }

def test_compression_decompression_cycle(test_cases):
    """Test that data remains intact after compression and decompression"""
    for test_data in test_cases:
        # Compress the data
        compressed = JsonCompressor.compress_json(test_data)
        
        # Verify compressed string is not empty and is a string
        assert isinstance(compressed, str)
        assert len(compressed) > 0
        
        # Decompress the data
        decompressed = JsonCompressor.decompress_json(compressed)
        
        # Verify the decompressed data matches original
        assert test_data == decompressed

def test_compression_reduces_size(large_data):
    """Test that compression actually reduces data size for large enough input"""
    original_size = len(json.dumps(large_data))
    compressed = JsonCompressor.compress_json(large_data)
    compressed_size = len(compressed)
    
    # Verify compression actually saved space
    assert compressed_size < original_size
