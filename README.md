# DHM Base Module

Basis modul som bygger på principper for software-opbygning, bl.a. anvendt i repositoriet "surfclass".

Build status: [![CircleCI](https://circleci.com/gh/Kortforsyningen/dhm-module-base.svg?style=svg)](https://circleci.com/gh/Kortforsyningen/dhm-module-base)

Dette er et basis modul, som er ment som modermodul for opgaver i SDFE. Funktionalitet der kunne have general betydning kan implementeres her, og specialiseret funktionalitet der enten lever i andre repositorier eller vil frembringe enten breaking changes / store dependency ændringer laves som plugins. Et eksempel på et modul der plugger ind i dette findes her: https://github.com/Kortforsyningen/dhm-module-example

CLI modulet er baseret på Click https://click.palletsprojects.com/en/7.x/

## Installation

### Conda Environment

```
git clone https://github.com/Kortforsyningen/dhm-module-base
cd dhm-module-base
conda env create -n dhm_module_base -f environment.yml
conda activate dhm_module_base
pip install .
```

Hvis man ønsker at udvikle på pluginnet, installeres da:

```
git clone https://github.com/Kortforsyningen/dhm-module-base
cd dhm-module-base
conda env create -n dhm_module_base -f environment-dev.yml
conda activate dhm_module_base
pip install -e .
```

## Brug af plugin

Modulet installerer sig selv som et python modul som sætter et entry point der kan kaldes på kommandolinjen. Modulet kommer ikke med nogle commands selv, disse skal oprettes enten via. plugins eller direkte på modulet, dette beskrives senere.

```
Usage: dhm_module_base [OPTIONS] COMMAND [ARGS]...

  dhm_module_base command line interface.

Options:
  --version                       Show the version and exit.
  -v, --verbosity [CRITICAL|ERROR|WARNING|INFO|DEBUG]
                                  Set verbosity level
  --help                          Show this message and exit.

Commands:
```

## Repositorie struktur

```
📦dhm-module-base
┣ 📂.circleci
┃ ┗ 📜config.yml # CircleCI Opsætning med status checks
┣ 📂.vscode
┃ ┗ 📜settings.json # .vscode settings, tilføjet i .gitignore
┣ 📂src # Dette er selve modulet
┃ ┣ 📂dhm_module_base
┃ ┃ ┣ 📜__init.py__ # __init__.py markerer mappen som en Python package
┃ ┃ ┣ 📜cli.py # Selve click CLI'en
┃ ┃ ┣ 📜helpers.py # Hjælpefunktioner såsom opsætning af logging
┃ ┃ ┣ 📜options.py # Opsætning af custom options
┣ 📂tests
┃ ┣ 📜__init__.py
┃ ┣ 📜conftest.py # Konfigurations objekter til pytest
┃ ┗ 📜test_cli.py # Simpel pytest der tester at cli virker
┣ 📜.gitignore
┣ 📜environment-dev.yml
┣ 📜environment.yml
┣ 📜LICENSE
┣ 📜README.md
┣ 📜setup.cfg # Indeholder repositorie specifikke regler vedrørende linting og docstrings
┗ 📜setup.py # setup.py indeholder metadata og indsætter entrypoints for modulet.
```

### `setup.py`

`setup.py` er en python fil der beskriver hvordan modulet i `src` skal installeres. Vi har fortalt python at `src\dhm_module_base` er et module da det har en `__init__.py` fil. Det vigtigste i `setup.py` for dette projekt er `ENTRY_POINTS`

Her beskriver vi at dette modul har ét entrypoint nemlig `dhm_module_base` som gør vi kan kalde CLI'en eksempelvis med `dhm_module_base --version`

```
ENTRY_POINTS = """
      [console_scripts]
      dhm_module_base=dhm_module_base.cli:cli
"""

```

### `with_plugins` opsætning af kommandoer i plugin

I `cli.py` registrerer vi en `click.group` og fortæller click at denne gruppe skal tage plugins med via dekoratoren `@with_plugins`

```
@with_plugins(iter_entry_points("dhm_module_base.plugins"))
@click.group("dhm_module_base")
```

Plugins skal nu i deres `setup.py` registrere kommandoer på `ENTRY_POINTS` således:

```
ENTRY_POINTS = """
      [dhm_module_base.plugins]
      inout=dhm_module_example.core:inout
      pipe=dhm_module_example.core:pipe
"""
```

Hvis plugins kan indlæses uden fejl vil de blive gjort tilgængelige på moder modulet som `commands`:

```
dhm_module_base

Options:
  --version                       Show the version and exit.
  -v, --verbosity [CRITICAL|ERROR|WARNING|INFO|DEBUG]
                                  Set verbosity level
  --help                          Show this message and exit.

Commands:
  inout  Example command inout.
  pipe   Example of a custom options handler being used along with a...
```

`inout` og `pipe` er kommandoer fra et andet plugin der bruger `[dhm_module_base.plugins]` entrypointet til at registrere sig i modermodulet. Se eksempel https://github.com/Kortforsyningen/dhm-module-example/blob/master/setup.py#L38

# Opsætning af Github og CircleCI for eksisterende python projekter

For eksisterende python projekter anbefales at anvende samme repositorie struktur med et (eller flere) moduler i `src` mappen, en `tests` mappe (uden `__init__.py`) og som det mindste en `setup.py`.

## Pytest

Pytest https://docs.pytest.org/en/latest/

Pytest kan både bruges til at skrive små tests til interne klasser, men også til at teste selve CLI. For eksempler på brugen af Pytest se https://github.com/Kortforsyningen/surfclass og dette moduls eksempel plugin https://github.com/Kortforsyningen/dhm-module-example. Det anbefales at hver kommando som det mindste testes igennem dets CLI, og gerne intern funktionalitet også.

Det anbefales at pytest sættes op i `.circleci\config.yml` som i dette repositorie

## Black formatting

Black https://black.readthedocs.io/en/stable/

Black er en automatisk kode-formatter der kan sættes op i eksempelvis Visual Studio Code eller køres på kommandolinjen med `black src`. Hvis formatteringen ikke finder nogle ændringer får man et output som dette:

```
$: black src

All done! ✨ � ✨
4 files left unchanged.
```

Black kan installeres med `pip install black` og er også inkluderet i conda environment beskrivelsen for dette projekt.

## Pydocstyle

Pydocstyle https://github.com/PyCQA/pydocstyle/ er et docstring modul der hjælper til at sørge for at docstrings overholder konventionerne. I dette repositorie er docstrings sat til overholde `google` docstring konventionen https://google.github.io/styleguide/pyguide.html#381-docstrings.

## CircleCI

CircleCI er i dette repositorie sat op med ét enkelt job `- lint_test_py37_conda` som tjekker at source-koden overholder reglerne for pylint, black, pydocstyle og at unit-tests ikke fejler. Det anbefales at repositoriets master holdes låst, og at ændringer køres igennem med reviewede pull-requests som består CircleCI tjekket. CircleCI opsætningen kan udvides til også at skubbe PyPi pakker.
