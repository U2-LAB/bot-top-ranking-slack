import pytest
from unittest.mock import Mock

from handlers.decorators import only_admin, poll_is_started, poll_not_started


def test_only_admin(mocker):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_send_msg = mocker.patch('handlers.decorators.send_msg_to_user')

    mocked_admin.return_value = True
    # Mock() is just test function that is wrapped in decorators.
    only_admin(Mock())(None, None, None)
    assert not mocked_send_msg.called