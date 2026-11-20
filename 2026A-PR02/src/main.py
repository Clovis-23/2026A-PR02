"""Lance l'interface NBA depuis le bon dossier."""

import os
import subprocess
import sys


def main() -> int:
    """Lance Streamlit et renvoie son code de sortie."""
    dossier_src = os.path.dirname(os.path.abspath(__file__))
    racine_projet = os.path.dirname(dossier_src)
    chemin_interface = os.path.join(dossier_src, "interface.py")

    resultat = subprocess.run(
        [sys.executable, "-m", "streamlit", "run", chemin_interface],
        cwd=racine_projet,
    )
    return resultat.returncode


if __name__ == "__main__":
    sys.exit(main())
