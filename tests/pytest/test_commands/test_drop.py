from handlers.commands import drop


def test_start_drop_as_admin(mocker, poll_for_tests):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_send_to_usr = mocker.patch('handlers.commands.drop.send_msg_to_user')
    
    mocked_admin.return_value = True
    drop.start_drop(None, poll_for_tests, None)
    assert mocked_send_to_usr.called