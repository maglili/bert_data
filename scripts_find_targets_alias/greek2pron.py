def greek2pron(text:str)->str:
    """
    Convert gerrk letters to english pronunciation.
    """
    dict = {
    'α':'alpha',
    'β':'beta',
    'γ':'gamma','Γ':'gamma',
    'Δ':'delta','δ':'delta',
    'ε':'epsilon',
    'ζ':'zeta',
    'η':'eta',
    'θ':'theta','Θ':'theta',
    'ι':'iota',
    'κ':'kappa',
    'Λ':'lambda','λ':'lambda',
    'μ':'mu',
    'ν':'nu',
    'ξ':'xi','Ξ':'xi',
    'π':'pi','Π':'pi',
    'ρ':'rho',
    'Σ':'sigma','σ':'sigma',
    'Τ':'tau','τ':'tau',
    'υ':'upsilon',
    'Φ':'phi','φ':'phi',
    'χ':'chi',
    'Ψ':'psi','ψ':'psi',
    'Ω':'omega','ω':'omega'
    }
    original = text
    text = text.lower()

    for i,j in dict.items():
        text = text.replace(i,j)

    return text

if __name__ == '__main__':
    print(greek2pron('eif2b ε'))
