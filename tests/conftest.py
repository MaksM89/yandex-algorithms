import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__name__), '../src'))


@pytest.fixture
def example_dir(monkeypatch: pytest.MonkeyPatch) -> Path:
    folder = Path(__file__).parent / 'example_dir'
    monkeypatch.chdir(folder)
    monkeypatch.syspath_prepend(folder)
    monkeypatch.delitem(sys.modules, 'conftest', raising=False)  # Удаляем загруженный pytest модуль
    return folder


@pytest.fixture
def cleanup_imports():
    """
    Фикстура сохраняет начальное состояние sys.modules и
    удаляет новые модули после теста.
    """
    initial_modules = set(sys.modules.keys())

    yield initial_modules

    # Удаляем модули, появившиеся во время теста
    current_modules = set(sys.modules.keys())
    new_modules = current_modules - initial_modules
    for modname in new_modules:
        sys.modules.pop(modname, None)


@pytest.fixture
def preserve_environ():
    original = dict(os.environ)  # Сохраняем копию
    yield
    # Восстанавливаем состояние
    os.environ.clear()
    os.environ.update(original)
