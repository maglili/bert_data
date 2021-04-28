def greek2pron(text: str) -> str:
    """
    Convert greek letters to english pronunciation.
    Only convert greek letters,some upper case greek letters will be ignore (e.g. A).

    Args:
        input:
            text(string): Greek letters that need to convert.
        return:
            text(string): English pronunciation.
    """
    dict = {
        "Α": "alpha",
        "α": "alpha",
        "Β": "beta",
        "β": "beta",
        "γ": "gamma",
        "Γ": "gamma",
        "Δ": "delta",
        "δ": "delta",
        "Ε": "epsilon",
        "ε": "epsilon",
        "Ζ": "zeta",
        "ζ": "zeta",
        "Η": "eta",
        "η": "eta",
        "θ": "theta",
        "Θ": "theta",
        "Ι": "iota",
        "ι": "iota",
        "Κ": "kappa",
        "κ": "kappa",
        "Λ": "lambda",
        "λ": "lambda",
        "Μ": "mu",
        "μ": "mu",
        "Ν": "nu",
        "ν": "nu",
        "Ξ": "xi",
        "ξ": "xi",
        "Ο": "omicron",
        "ο": "omicron",
        "Π": "pi",
        "π": "pi",
        "Ρ": "rho",
        "ρ": "rho",
        "Σ": "sigma",
        "σ": "sigma",
        "ς": "sigma",
        "Ϲ": "sigma",
        "ϲ": "sigma",
        "Τ": "tau",
        "τ": "tau",
        "Y": "upsilon",
        "υ": "upsilon",
        "Φ": "phi",
        "φ": "phi",
        "Χ": "chi",
        "χ": "chi",
        "Ψ": "psi",
        "ψ": "psi",
        "Ω": "omega",
        "ω": "omega",
    }
    original = text
    text = text.lower()

    for i, j in dict.items():
        text = text.replace(i, j)

    return text


if __name__ == "__main__":
    print(greek2pron("eif2b ε"))
    print(greek2pron("ABCDEFGHIJKLMNOPQRXTUVWXYZ"))
    print(greek2pron("Α Β Ε Ζ Η Ι Κ Μ Ν ν Ο ο Ρ Τ Υ υ Χ Ω"))
