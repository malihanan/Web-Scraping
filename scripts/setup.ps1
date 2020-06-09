py -m venv env
./env/Scripts/activate
pip install -r resources/requirements.txt
python src/generate_options.py
scripts/scrape.ps1