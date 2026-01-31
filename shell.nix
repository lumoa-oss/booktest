{
  pkgs ? import <nixpkgs> {},
  unstable ? import <nixos-unstable> { inherit (pkgs) system; config.allowUnfree = true; }
}:

pkgs.mkShell {
  buildInputs = [
    # Python
    pkgs.python312

    # Native libraries needed by numpy/pandas C extensions
    pkgs.stdenv.cc.cc.lib
    pkgs.zlib

    # Python development tools
    pkgs.uv

    unstable.claude-code

    # IDE
    pkgs.jetbrains.pycharm-community

    # Development tools
    pkgs.git
    pkgs.curl
    pkgs.wget
    pkgs.gh

    # Shell utilities
    pkgs.zsh
    pkgs.direnv
  ];

  shellHook = ''
    # Make native libraries visible to Python packages (numpy, pandas)
    export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:$LD_LIBRARY_PATH"

    echo "📖 Booktest Development Environment"
    echo "===================================="
    echo "Python: $(python --version)"
    echo "uv: $(uv --version)"
    echo ""
    echo "To start PyCharm: pycharm-community ."
    echo ""

    # Activate virtual environment
    if [ ! -d ".venv" ]; then
      echo "Creating virtual environment..."
      uv sync
    fi

    source .venv/bin/activate

    echo "✓ Virtual environment activated"
    echo ""
    echo "Quick commands:"
    echo "  uv sync          - Install/sync dependencies"
    echo "  uv run <cmd>     - Run command in project environment"
    echo "  ./do test        - Run tests"
    echo "  ./do lint        - Run linter"
    echo "  ./do qa          - Run lint + tests"
  '';
}
