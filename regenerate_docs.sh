# Build low level docs

## Run this command if we want to update per-method and per-class docstrings
# python -m automata.cli.scripts.run_docs_l1 --top_n_symbols=100 --update_docs 

## Run this command to constract a map of class symbols to documentation
python -m automata_docs.cli.scripts.run_docs_l2 --top_n_symbols=2 --update_docs 

## Run this command to aggregate documentation into directory structure
# doc_gen = PythonDocumentWriter(relative_dir)
# doc_gen.write_documentation(docs, keys, relative_dir)

# Build aggregate docs
# ...

# Remove local doc .rst files and re-create
# ...

# # remove existing docs in the doc repo
rm -rf ../automata-docs-repo/docs/*

# # copy latest docs over
cp -rf local_env/docs/* ../automata-docs-repo/docs
