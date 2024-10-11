{ pkgs, ... }: {
  channel = "stable-23.11";

  packages = [
    pkgs.nodejs_20
  ];

  env = {
    MONGODB_CONNECTION_STRING = "mongodb://localhost:27017/";
  };

  services.mongodb = {
    enable = true;
  };

  idx = {
    extensions = [
      "mongodb.mongodb-vscode"
    ];

    workspace = {
      onCreate = {
        npm-install = "npm install";
        default.openFiles = [
          "server.js" "database.js"
        ];
      };
      onStart = {
        start-database = "mongod --port 27017 --fork --logpath ./.idx/database.log --dbpath ./.idx/.data";
        run-index = "node server.js";
      };
    };

    previews = {
      enable = true;
      previews = {
      };
    };
  };
}
