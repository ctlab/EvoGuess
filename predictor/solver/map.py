from .impls.cadical import CadicalSolver
from .impls.cryptominisat import CryptoMinisatSolver
from .impls.lingeling import LingelingSolver
from .impls.maplesat import MapleSATSolver
from .impls.minisat import MinisatSolver
from .impls.painless import PainlessSolver
from .impls.plingeling import PlingelingSolver
from .impls.rokk import RokkSolver
from .impls.treengeling import TreengelingSolver

solvers = {
    "minisat": MinisatSolver,
    "lingeling": LingelingSolver,
    "plingeling": PlingelingSolver,
    "treengeling": TreengelingSolver,
    "cryptominisat": CryptoMinisatSolver,
    "rokk": RokkSolver,
    "maplesat": MapleSATSolver,
    "painless": PainlessSolver,
    "cadical": CadicalSolver
}


def get_solver(options):
    return solvers[options['name']](**options)
