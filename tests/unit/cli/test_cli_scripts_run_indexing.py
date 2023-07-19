from unittest.mock import patch, call
from automata.cli.scripts import run_indexing


def test_main():
    with patch('os.path.dirname') as mock_dirname, \
            patch('os.path.join') as mock_join, \
            patch('subprocess.check_call') as mock_check_call:

        # Configure mocks
        mock_dirname.return_value = '/mock/directory'
        mock_join.side_effect = [
            '/mock/directory/../../../scripts',
            '/mock/directory/../../../scripts/install_indexing.sh',
            '/mock/directory/../../../scripts/regenerate_index.sh',
        ]

        # Call main
        run_indexing.main()

        # Assertions
        mock_dirname.assert_called_once_with(run_indexing.__file__)
        assert mock_join.call_args_list == [
            call(mock_dirname.return_value, "../../../scripts"),
            call('/mock/directory/../../../scripts', "install_indexing.sh"),
            call('/mock/directory/../../../scripts', "regenerate_index.sh"),
        ]
        assert mock_check_call.call_args_list == [
            call(['sh', '/mock/directory/../../../scripts/install_indexing.sh']),
            call(['sh', '/mock/directory/../../../scripts/regenerate_index.sh']),
        ]
