{
  description = "Automata";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python310;
        pythonPkgs = pkgs.python310Packages;
        pythonEnv = python.withPackages (ps: with ps;
          [
            black
            click
            codecov
            colorlog
            isort
            jinja2
            jsonpickle
            jsonschema
            matplotlib
            networkx
            numpy
            openai
            pandas
            plotly
            protobuf
            pydantic
            pypandoc
            pytest-mock
            python-dotenv
            redbaron
            scikit-learn
            scipy
            termcolor
            tiktoken
            types-protobuf
            gitpython
            pygithub
            pyyaml
            jupyter
            notebook
          ]);
      in
      {
        # Create a devShell with the Python environment and some tools
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            yapf
            jupyter
          ];
          shellHook = ''
            export PYTHONPATH=${pythonEnv}/bin/python
          '';
        };
      }
    );
}

