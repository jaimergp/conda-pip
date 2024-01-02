import pytest

from conda.base.context import reset_context
from conda.core.prefix_data import PrefixData
from conda.exceptions import CondaError
from conda.testing import CondaCLIFixture, TmpEnvFixture
from conda.testing.integration import package_is_installed


def test_pip_required_in_target_env(tmp_env: TmpEnvFixture, conda_cli: CondaCLIFixture, monkeypatch):
    monkeypatch.setenv("CONDA_ADD_PIP_AS_PYTHON_DEPENDENCY", "false")
    reset_context()
    with tmp_env("xz") as prefix:
        args = ("pip", "-p", prefix, "--yes", "install", "requests")
        
        with pytest.raises(CondaError, match="does not have Python installed"):
            out, err, rc = conda_cli(*args)
        out, err, rc = conda_cli("install", "-p", prefix, "--yes", "python=3.9")
        PrefixData._cache_.clear()  # clear cache to force re-read of prefix
        assert package_is_installed(str(prefix), "python=3.9")
        assert not package_is_installed(str(prefix), "pip")
        PrefixData._cache_.clear()

        with pytest.raises(CondaError, match="does not have pip installed"):
            out, err, rc = conda_cli(*args)
        out, err, rc = conda_cli("install", "-p", prefix, "--yes", "pip")
        PrefixData._cache_.clear()  # clear cache to force re-read of prefix
        assert package_is_installed(str(prefix), "pip")
        PrefixData._cache_.clear()
        
        out, err, rc = conda_cli(*args)
        PrefixData._cache_.clear()
        assert rc == 0
        assert package_is_installed(str(prefix), "requests")
    monkeypatch.undo()
    reset_context()