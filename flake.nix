{
  description = "Development environment for airlift";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.python310
            pkgs.poetry
            pkgs.kubernetes-helm
            pkgs.docker
            pkgs.kind
            pkgs.ruff
            pkgs.black
          ];

          shellHook = ''
            echo "    _   _     _ _  __ _   "
            echo "   /_\ (_)_ _| (_)/ _| |_ "
            echo "  / _ \| | '_| | |  _|  _|"
            echo " /_/ \_\_|_| |_|_|_|  \__|"
            echo "Welcome to the development environment for Airlift!"
            echo ""
            echo "👉 To get started, run 'poetry install' to install dependencies."
            echo "👉 After installing dependencies, run 'poetry shell' to open your shell with those dependencies activated."
            echo ""
            echo "ℹ️ When you are ready to test your changes, run 'poetry build' and then 'pip install dist/airlift*.whl' to install the airlift CLI with your changes"
          '';
        };
      }
    );
}
