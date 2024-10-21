{ pkgs, ... }: {
  channel = "stable-23.11";

  packages = [
    pkgs.python3
  ];

  services.mongodb = {
    enable = true;
  };

  idx = {
    extensions = [
      "ms-python.python"
      "mongodb.mongodb-vscode"
    ];

    workspace = {
      onCreate = {
        install = "python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt";
        default.openFiles = [
          "app.py" "README.md"
        ];
      };
      onStart = {
        start-database = "mongod --port 27017 --fork --logpath ./.idx/database.log --dbpath ./.idx/.data";
        run-server = "./devserver.sh";
      };
    };

    previews = {
      enable = true;
      previews = {
      };
    };
  };
}
