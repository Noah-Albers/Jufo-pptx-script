from tqdm import tqdm

def inform_user(iterator, infos: str = "Doing something"):
    return tqdm(iterator, desc=infos)
