import pickle
from pathlib import Path
import streamlit_authenticator as auth


unames = []
psswds = []
hashed_psswds = auth.Hasher(psswds).generate()
file_path = Path(__file__).parent / 'hashed_psswds.pkl'

with file_path.open('wb') as f:
    pickle.dump(hashed_psswds, f)
