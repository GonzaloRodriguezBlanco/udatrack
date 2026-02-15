import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker
import uuid

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

@pytest.fixture
def default_id():
    return str(uuid.uuid4())

@pytest.fixture
def order_default(default_id):
    """
    Provides a order string for testing.
    """
    return {
        "order_id": default_id,
        "item_name": 'jacket',
        "quantity": 1,
        "customer_id": default_id,
    }
#
# --- TODO: add test functions below this line ---
#
def test_add_order_without_status_creates_order_with_status_pending(order_tracker):
    # Arrange
    mock_storage = order_tracker.storage

    order_id = str(uuid.uuid4())
    customer_id = str(uuid.uuid4())

    # Act
    order_tracker.add_order(
        order_id,
        'jacket',
        1,
        customer_id
    )

    # Assert
    mock_storage.save_order.assert_called_once()
    mock_storage.save_order.assert_called_with(
        order_id,
        dict(
            order_id=order_id,
            item_name='jacket',
            quantity=1,
            customer_id = customer_id,
            status='pending'
        )
    )

@pytest.mark.parametrize("status", [
    'pending',
    'processing'
])
def test_add_order_with_explicit_shipped_status(order_tracker, mock_storage, order_default, status):
    # Arrange
    order_id = order_default.get('order_id')
    order = dict(order_default, status=status)

    # Act
    order_tracker.add_order(
        order_id,
        order.get('item_name'),
        order.get('quantity'),
        order.get('customer_id'),
        order.get('status')
    )

    # Assert
    mock_storage.save_order.assert_called_once()
    mock_storage.save_order.assert_called_with(order_id, order)

# DONE duplicate IDs
def test_add_order_with_duplicate_id_raise_exception(order_tracker, order_default):
     # Arrange
     order_duplicated = order_default.copy()
     mock_storage = order_tracker.storage
     mock_storage.get_order.side_effect = [None, order_default]

     order_tracker.add_order(
         order_default.get('order_id'),
         order_default.get('item_name'),
         order_default.get('quantity'),
         order_default.get('customer_id')
     )
     order_id = order_default.get('order_id')

     # Act
     with pytest.raises(ValueError, match=f"Order with ID '{order_id}' already exists."):
         order_tracker.add_order(
             order_id,
             order_duplicated.get('item_name'),
             order_duplicated.get('quantity'),
             order_duplicated.get('customer_id')
         )

     # Assert
     assert mock_storage.get_order.call_count == 2
     assert mock_storage.save_order.call_count == 1

# DONE invalid quantity
@pytest.mark.parametrize("quantity", [0, -1])
def test_add_order_with_invalid_quantity_should_raise_error(order_tracker, quantity, order_default):
    # Act
    with pytest.raises(ValueError, match=f"Minimum quantity value allowed {order_tracker.MIN_QUANTITY_ALLOWED}, {quantity} given."):
        order_tracker.add_order(
            order_default.get('order_id'),
            order_default.get('item_name'),
            quantity,
            order_default.get('customer_id')
        )

# DONE missing required fields
@pytest.mark.parametrize("order,error_message", [
    (dict(item_name="jacket", quantity=1, customer_id=str(uuid.uuid4())),
     "missing 1 required positional argument: 'order_id'"),
    (dict(order_id=str(uuid.uuid4()), quantity=1, customer_id=str(uuid.uuid4())),
     "missing 1 required positional argument: 'item_name'"),
    (dict(order_id=str(uuid.uuid4()), item_name='jacket', customer_id=str(uuid.uuid4())),
     "missing 1 required positional argument: 'quantity'"),
    (dict(order_id=str(uuid.uuid4()), item_name='jacket', quantity=1),
     "missing 1 required positional argument: 'customer_id'"),
    (dict(item_name='jacket', customer_id=str(uuid.uuid4())),
     "missing 2 required positional arguments: 'order_id' and 'quantity'"),
])
def test_add_oder_without_required_fields_should_raise_error(order_tracker, order, error_message):
    # Act
    with pytest.raises(TypeError, match=error_message):
        order_tracker.add_order(**order)

# DONE invalid initial status. Considering valid initial pending and processing.
@pytest.mark.parametrize("status", [
    'shipped',
    'delivered',
    'cancelled'
])
def test_add_order_with_invalid_initial_status_raise_error(order_tracker, order_default, status):
    # Arrange
    order_default['status'] = status

    # Act
    with pytest.raises(ValueError, match=f"Invalid initial status, allowed '{", ".join(order_tracker.INITIAL_STATUS_ALLOWED)}' but  '{status}' given."):
        order_tracker.add_order(**order_default)

# DONE: Fetch existing order id returns order by its ID or return None if it doesn't exist
def test_fetch_by_existing_order_id_returns_order(order_tracker, order_default):
    # Arrange
    mock_storage = order_tracker.storage
    mock_storage.get_order.return_value = order_default
    order_id = order_default.get('order_id')

    # Act
    order_actual = order_tracker.get_order_by_id(order_id)

    # Assert
    mock_storage.get_order.assert_called_once()
    mock_storage.get_order.assert_called_with(order_id)
    assert order_actual == order_default

# DONE: Fetch non-existing order id returns None
def test_fetch_by_non_existing_order_id_returns_none(order_tracker):
    # Arrange
    # Act
    order = order_tracker.get_order_by_id("non_existing_order_id")
    # Assert
    assert order is None

# DONE: not present required argument order ID should raise exception
def test_not_present_required_argument_order_id_should_raise_error(order_tracker):
    # Act
    with pytest.raises(TypeError, match="missing 1 required positional argument: 'order_id'"):
        order_tracker.get_order_by_id()

# DONE: Empty ID should raise exception
def test_fetch_by_empty_id_should_raise_error(order_tracker):
    # Arrange
    empty_id = ""

    # Act
    with pytest.raises(ValueError, match="'order_id' cannot be empty."):
        order_tracker.get_order_by_id(empty_id)

# DONE: update_order_status success_path
@pytest.mark.parametrize("existing_order,new_status", [
    (dict(order_id='order-id', item_name='jacket', quantity=1, customer_id='customer_id', status='pending'), 'cancelled'),
    (dict(order_id='order-id', item_name='jacket', quantity=1, customer_id='customer_id', status='pending'), 'processing'),
    (dict(order_id='order-id', item_name='jacket', quantity=1, customer_id='customer_id', status='processing'), 'cancelled'),
    (dict(order_id='order-id', item_name='jacket', quantity=1, customer_id='customer_id', status='processing'), 'shipped'),
    (dict(order_id='order-id', item_name='jacket', quantity=1, customer_id='customer_id', status='shipped'), 'delivered')
])
def test_update_order_status_sucess(order_tracker, existing_order, new_status):
    # Arrange
    mock_storage = order_tracker.storage
    mock_storage.get_order.return_value = existing_order

    # Act
    order_tracker.update_order_status(existing_order['order_id'], new_status)

    # Assert
    mock_storage.get_order.assert_called_once()
    mock_storage.get_order.assert_called_with(existing_order['order_id'])
    mock_storage.save_order.assert_called_once_with(existing_order['order_id'], dict(existing_order, status=new_status))

# DONE: invalid status (fail fast, no storage read)
def test_update_order_with_invalid_status_should_raise_error(order_tracker):
    # Arrange
    invalid_status = "invalid"

    # Act
    with pytest.raises(ValueError, match=f"Not a valid status. Allowed values '{", ".join(order_tracker.VALID_STATUS_ALLOWED)}' but '{invalid_status}' given"):
        order_tracker.update_order_status('order_id', invalid_status)

# DONE: update_order_status non existent order
def test_update_order_status_with_not_found_order_should_raise_error(order_tracker):
    # Arrange
    non_existing_order_id = 'non_existing_id'

    # Act
    with pytest.raises(Exception, match=f"Order with ID '{non_existing_order_id}' not found."):
        order_tracker.update_order_status(non_existing_order_id, 'shipped')

# DONE: update_order_status empty order id should raise error
def test_update_order_status_with_empty_order_id_should_raise_error(order_tracker):
    # Arrange
    empty_id = ""

    # Act
    with pytest.raises(ValueError, match="'order_id' cannot be empty."):
        order_tracker.update_order_status(empty_id, 'shipped')