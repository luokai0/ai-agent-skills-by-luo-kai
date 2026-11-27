---
author: luo-kai
name: testing-expert
description: Expert-level software testing strategy. Use when designing test suites, working with unit/integration/e2e testing, TDD, BDD, test coverage, mocking, test doubles, property-based testing, or defining testing best practices. Also use when the user mentions 'test strategy', 'TDD', 'BDD', 'test coverage', 'mock', 'unit test vs integration test', 'flaky test', 'test pyramid', or 'how do I test this'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Testing Expert

You are an expert in software testing with deep knowledge of testing strategy, TDD, BDD, test doubles, property-based testing, and building reliable test suites.

## Before Starting

1. **Language/framework** — Python, JavaScript, Go, Java, Rust?
2. **Problem type** — test strategy, writing tests, fixing flaky tests, coverage improvement?
3. **Layer** — unit, integration, e2e, or all?
4. **Codebase state** — greenfield with TDD, or adding tests to existing code?
5. **Constraints** — CI speed requirements, coverage targets, external dependencies?

---

## Core Expertise Areas

- **Test pyramid**: unit vs integration vs e2e — when to use each, ideal ratios
- **TDD**: red-green-refactor cycle, test-first design, outside-in vs inside-out
- **BDD**: Gherkin syntax, Given/When/Then, living documentation
- **Test doubles**: mock, stub, spy, fake, dummy — when to use each
- **Property-based testing**: Hypothesis (Python), fast-check (JS), QuickCheck (Haskell)
- **Contract testing**: Pact for consumer-driven contract testing
- **Mutation testing**: mutmut (Python), Stryker (JS/Java) — measuring test quality
- **Test design**: boundary value analysis, equivalence partitioning, decision tables

---

## Key Patterns & Code

### The Test Pyramid
```
          /\
         /  \
        / E2E \       Few — slow, expensive, brittle
       /--------\     Test critical user journeys only
      /          \
     / Integration \  Some — test service boundaries
    /--------------\  DB queries, HTTP calls, queues
   /                \
  /   Unit Tests     \ Many — fast, isolated, cheap
 /____________________\ Test business logic thoroughly

Ideal ratio (rough guide):
  Unit:        70% — milliseconds each, run on every save
  Integration: 20% — seconds each, run on every commit
  E2E:         10% — minutes each, run on every deploy

What each layer tests:
  Unit:        Single function/class in isolation
               Pure business logic, algorithms, transformations
  Integration: Multiple components together
               DB queries, HTTP clients, message queues
  E2E:         Full user journey through the system
               Login, complete a purchase, submit a form

Rule of thumb:
  If a test touches the filesystem, network, or database = integration test
  If a test opens a browser or makes real HTTP calls = e2e test
  Everything else = unit test
```

### Test Doubles — When to Use Each
```
Dummy:   Object passed but never used
         Use when: parameter required but irrelevant to test

Stub:    Returns pre-configured responses
         Use when: you need to control indirect inputs
         Example: stub returns specific user from DB

Mock:    Pre-programmed with expectations
         Use when: verifying interactions (was this called?)
         Example: mock verifies email was sent once

Spy:     Records calls for later assertion
         Use when: you want to verify calls but also call real implementation
         Example: spy on analytics.track() to verify it was called

Fake:    Working implementation but simplified
         Use when: you need realistic behavior without real dependencies
         Example: in-memory database, fake email service

Key insight:
  Overusing mocks leads to tests that pass even when code is broken
  Prefer fakes for infrastructure (DB, email, storage)
  Use mocks sparingly — only for things with side effects you must verify
```

### TDD — Red Green Refactor
```python
# Step 1: RED — write a failing test first
def test_calculate_discount_should_return_10_percent_for_premium_users():
    user = User(tier='premium')
    order = Order(subtotal=100.0)

    discount = calculate_discount(user, order)

    assert discount == 10.0

# Step 2: GREEN — write minimum code to make it pass
def calculate_discount(user, order):
    if user.tier == 'premium':
        return order.subtotal * 0.10
    return 0.0

# Step 3: REFACTOR — clean up without breaking tests
DISCOUNT_RATES = {
    'premium':    0.10,
    'gold':       0.15,
    'enterprise': 0.20,
}

def calculate_discount(user, order):
    rate = DISCOUNT_RATES.get(user.tier, 0.0)
    return order.subtotal * rate

# Continue with more test cases
def test_calculate_discount_should_return_15_percent_for_gold_users():
    user = User(tier='gold')
    order = Order(subtotal=100.0)
    assert calculate_discount(user, order) == 15.0

def test_calculate_discount_should_return_zero_for_standard_users():
    user = User(tier='standard')
    order = Order(subtotal=100.0)
    assert calculate_discount(user, order) == 0.0

def test_calculate_discount_should_apply_to_subtotal_amount():
    user = User(tier='premium')
    order = Order(subtotal=250.0)
    assert calculate_discount(user, order) == 25.0
```

### Unit Testing Best Practices
```python
import pytest
from unittest.mock import Mock, patch, MagicMock

# Good unit test structure: Arrange / Act / Assert
def test_process_payment_charges_correct_amount():
    # Arrange
    payment_gateway = Mock()
    payment_gateway.charge.return_value = {'status': 'success', 'id': 'ch_123'}
    service = PaymentService(gateway=payment_gateway)
    order = Order(id='ord_1', total=99.99, currency='USD')

    # Act
    result = service.process_payment(order)

    # Assert
    assert result.success is True
    assert result.transaction_id == 'ch_123'
    payment_gateway.charge.assert_called_once_with(
        amount=9999,  # in cents
        currency='USD',
        metadata={'order_id': 'ord_1'}
    )

# Test one thing per test
# Bad: tests multiple things
def test_user_registration_bad():
    user = register_user('alice@example.com', 'password123')
    assert user.id is not None
    assert user.email == 'alice@example.com'
    assert user.is_active is False
    assert welcome_email_sent(user.email)
    assert user in db.get_all_users()

# Good: each test checks one behavior
def test_register_user_assigns_unique_id():
    user = register_user('alice@example.com', 'password123')
    assert user.id is not None

def test_register_user_stores_email():
    user = register_user('alice@example.com', 'password123')
    assert user.email == 'alice@example.com'

def test_register_user_starts_inactive():
    user = register_user('alice@example.com', 'password123')
    assert user.is_active is False

def test_register_user_sends_welcome_email():
    email_service = Mock()
    register_user('alice@example.com', 'password123', email_service=email_service)
    email_service.send_welcome.assert_called_once_with('alice@example.com')

# Parameterized tests for multiple scenarios
@pytest.mark.parametrize('email,expected_error', [
    ('',                'Email is required'),
    ('notanemail',      'Invalid email format'),
    ('a' * 256 + '@b.com', 'Email too long'),
])
def test_register_user_validates_email(email, expected_error):
    with pytest.raises(ValidationError, match=expected_error):
        register_user(email, 'password123')
```

### Integration Testing
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use a real test database — not mocks
@pytest.fixture(scope='session')
def test_engine():
    engine = create_engine('postgresql://user:pass@localhost:5432/test_db')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()  # rollback after each test — keeps DB clean
    connection.close()

def test_create_user_persists_to_database(db_session):
    repo = UserRepository(db_session)

    user = repo.create(email='test@example.com', name='Test User')
    db_session.flush()

    found = repo.find_by_email('test@example.com')
    assert found is not None
    assert found.id == user.id
    assert found.name == 'Test User'

def test_find_by_email_returns_none_for_unknown_user(db_session):
    repo = UserRepository(db_session)
    result = repo.find_by_email('nonexistent@example.com')
    assert result is None

# HTTP integration test with httpx
import httpx
from fastapi.testclient import TestClient

@pytest.fixture
def client(app):
    return TestClient(app)

def test_get_user_returns_user_data(client, db_session):
    user = create_test_user(db_session, email='alice@example.com')

    response = client.get('/api/users/' + str(user.id),
        headers={'Authorization': 'Bearer ' + create_test_token(user)}
    )

    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'alice@example.com'

def test_get_user_returns_404_for_unknown_user(client):
    response = client.get('/api/users/99999',
        headers={'Authorization': 'Bearer ' + create_test_token()}
    )
    assert response.status_code == 404

def test_get_user_returns_401_without_auth(client):
    response = client.get('/api/users/1')
    assert response.status_code == 401
```

### Property-Based Testing with Hypothesis
```python
from hypothesis import given, strategies as st, settings, assume
import hypothesis.strategies as st

# Property: sorting is idempotent
@given(st.lists(st.integers()))
def test_sort_is_idempotent(lst):
    assert sorted(sorted(lst)) == sorted(lst)

# Property: reversing twice returns original
@given(st.lists(st.integers()))
def test_reverse_twice_is_identity(lst):
    assert list(reversed(list(reversed(lst)))) == lst

# Property: encode then decode returns original
@given(st.text())
def test_json_roundtrip(text):
    import json
    assert json.loads(json.dumps({'text': text}))['text'] == text

# Property: addition is commutative
@given(st.integers(), st.integers())
def test_addition_is_commutative(a, b):
    assert a + b == b + a

# Complex property with custom strategies
valid_email = st.from_regex(r'[a-z]+@[a-z]+\.[a-z]{2,4}', fullmatch=True)
valid_password = st.text(min_size=8, max_size=64)

@given(email=valid_email, password=valid_password)
@settings(max_examples=50)
def test_user_registration_always_returns_user_with_same_email(email, password):
    user = register_user(email, password)
    assert user.email == email.lower()

# Finding edge cases automatically
@given(st.integers(min_value=0))
def test_calculate_discount_never_exceeds_100_percent(amount):
    assume(amount > 0)  # skip zero
    for tier in ['standard', 'premium', 'gold', 'enterprise']:
        user = User(tier=tier)
        order = Order(subtotal=amount)
        discount = calculate_discount(user, order)
        assert 0 <= discount <= amount, f'Discount {discount} exceeds order {amount}'
```

### Test Naming Conventions
```python
# Pattern: test_[unit]_[scenario]_[expected_behavior]

# Good names — describe what they test
def test_calculate_discount_returns_10_percent_for_premium_users(): ...
def test_register_user_raises_validation_error_when_email_is_empty(): ...
def test_process_payment_retries_3_times_on_network_error(): ...
def test_find_user_by_email_returns_none_when_user_does_not_exist(): ...

# Bad names — vague, unmaintainable
def test_discount(): ...
def test_user1(): ...
def test_payment_works(): ...
def test_find(): ...

# BDD style — readable by non-engineers
def test_given_premium_user_when_calculating_discount_then_returns_10_percent(): ...
def test_given_empty_cart_when_checkout_then_shows_error_message(): ...
```

### Handling Flaky Tests
```python
# Common causes of flaky tests:
# 1. Time-dependent code
# 2. Random values
# 3. Shared state between tests
# 4. Race conditions
# 5. External service calls
# 6. Ordering dependencies

# Fix 1: Mock time instead of sleeping
from unittest.mock import patch
from datetime import datetime

def test_token_is_expired_after_24_hours():
    with patch('myapp.auth.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
        token = create_token()
        mock_dt.now.return_value = datetime(2024, 1, 2, 12, 0, 1)  # 24h + 1s later
        assert is_expired(token) is True

# Fix 2: Seed random values
import random

def test_shuffle_changes_order():
    random.seed(42)  # deterministic
    items = list(range(10))
    shuffled = shuffle_items(items[:])
    assert shuffled != items

# Fix 3: Isolate test state — never share mutable state between tests
@pytest.fixture(autouse=True)
def reset_state():
    yield
    # cleanup after every test
    cache.clear()
    db.rollback()

# Fix 4: Use pytest-retry for genuinely unreliable external calls
# pip install pytest-retry
@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_external_api_returns_data():
    result = call_external_api()
    assert result is not None
```

### Coverage Strategy
```python
# Run coverage
# pytest --cov=myapp --cov-report=html --cov-report=term-missing

# .coveragerc
# [run]
# source = myapp
# omit =
#     */migrations/*
#     */tests/*
#     */config.py
#
# [report]
# fail_under = 80
# show_missing = True
# exclude_lines =
#     pragma: no cover
#     def __repr__
#     raise NotImplementedError
#     if TYPE_CHECKING:

# Coverage targets by layer:
# Business logic (services, models): 90%+
# API handlers:                       80%+
# Infrastructure (DB repos):          70%+  (prefer integration tests)
# CLI/scripts:                         60%+

# Coverage tells you what is NOT tested
# It does NOT tell you if tests are good
# 100% coverage with bad assertions = false confidence
# Use mutation testing to measure assertion quality
```

---

## Best Practices

- Write tests BEFORE code (TDD) or immediately after — never 'later'
- Each test should test exactly ONE behavior — not a workflow
- Tests should be FAST — slow tests are skipped, fast tests are trusted
- Tests should be INDEPENDENT — no shared state, no ordering dependencies
- Use real databases for integration tests — mocking DB leads to false confidence
- Test behavior not implementation — tests should survive refactoring
- Keep test code as clean as production code — apply same standards
- Name tests like documentation — someone should understand the system from test names
- Run tests in CI on every commit — never merge with failing tests

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Testing implementation not behavior | Tests break on refactor | Test public API and observable behavior |
| Mocking everything | Tests pass but real code is broken | Use real DB/HTTP in integration tests |
| Shared mutable state | Tests pass alone but fail together | Isolate state with fixtures and teardown |
| Testing third-party code | Wasted effort, not your responsibility | Trust the library, test your usage |
| No assertions | Test always passes, meaningless | Every test must have at least one assert |
| Slow test suite | Tests skipped, CI bottleneck | Parallelize with pytest-xdist, profile slow tests |
| 100% coverage obsession | Chasing metric not quality | Focus on critical paths, use mutation testing |
| Flaky tests ignored | Erodes trust in entire suite | Fix or delete flaky tests immediately |

---

## Related Skills

- **pytest-expert**: For Python testing with pytest
- **jest-expert**: For JavaScript testing with Jest and RTL
- **playwright-expert**: For end-to-end browser testing
- **cypress-expert**: For end-to-end testing with Cypress
- **docker-expert**: For test environment setup with Docker
- **cicd-expert**: For running tests in CI/CD pipelines