from jufo_pptx_script.common.jufo.JufoConstants import FACHBEREICHE, SPARTEN


def validate_fachbereich_and_sparte(fb: str, sparte: str):
    if not fb in FACHBEREICHE:
        raise ValueError(f"Invalider Fachbereich '{fb}' angegeben.")
    if not sparte in SPARTEN:
        raise ValueError(f"Invalide Sparte '{sparte}' angegeben.")