### Usage
```
python3 search_file.py index --path /user/name/path/to/folder
python3 search_file.py search --query “sickness”

To keep a background updater and live use in terminal:
python3 seman_search.py --path /user/folder/to/semanticSearch
```

### Dependencies
```
pip3 install -U sentence-transformers
pip3 install faiss-cpu
pip3 install watchdog
```
https://pypi.org/project/sentence-transformers/

https://pypi.org/project/faiss-cpu/

### TODO
1. GUI
2. Optimization
3. Expand search scope to file internals

### Sid TODO
1. automatic indexing when files are added/removed [COMPLETED]
2. Terminal GUI to query faster than rerunning long terminal prompt [Completed] - set to seman_search.py
