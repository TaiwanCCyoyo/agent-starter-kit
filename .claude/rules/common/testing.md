# Testing Requirements

## Minimum Coverage: 80%

All three test types are required:
1. **Unit** — individual functions and utilities
2. **Integration** — API endpoints, database operations
3. **E2E** — critical user flows

TDD workflow is provided by `superpowers: test-driven-development`. Repository-specific test commands are in `skill: python-testing`.

## Test Structure (AAA Pattern)

```python
def test_calculates_similarity_correctly():
    # Arrange
    vector1 = [1, 0, 0]
    vector2 = [0, 1, 0]

    # Act
    similarity = calculate_cosine_similarity(vector1, vector2)

    # Assert
    assert similarity == 0
```

## Test Naming

Use descriptive names that explain the behavior under test:

```python
def test_returns_empty_list_when_no_markets_match_query(): ...
def test_raises_value_error_when_api_key_is_missing(): ...
def test_falls_back_to_substring_search_when_redis_is_unavailable(): ...
```
