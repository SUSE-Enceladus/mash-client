import json
import os
import yaml

from mash_client.cli import main
from click.testing import CliRunner


def test_setup_and_show_config():
    """Test mash setup and show config."""
    runner = CliRunner()

    with runner.isolated_filesystem():
        os.makedirs('tests/data/')
        result = runner.invoke(
            main,
            ['config', 'setup'],
            input='tests/data/\n'
                  '\n'
                  'test@test.com\n'
                  '\n'
                  '\n'
                  '\n'
                  'n\n'
                  'y\n'
                  '/path/to/cert\n'
        )

        assert result.exit_code == 0

        result = runner.invoke(
            main,
            ['-C', 'tests/data/', 'config', 'show']
        )

        assert result.exit_code == 0

        data = json.loads(result.output)

        assert data['host'] == 'http://127.0.0.1'
        assert data['log_level'] == 20
        assert data['no_color']
        assert data['verify'] == '/path/to/cert'
        assert data['email'] == 'test@test.com'

        with open('tests/data/default.yaml') as config_file:
            config_values = yaml.safe_load(config_file)

    assert config_values['email'] == 'test@test.com'
    assert config_values['verify'] == '/path/to/cert'
