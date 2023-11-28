from distutils.util import subst_vars
import os

BasePath = "structure"

FileList = [
    ".babelrc",
    ".dockerignore",
    ".env",
    ".gitignore",
    "docker-compose.yml",
    "Dockerfile",
    "Jenkinsfile",
    "modules.d.ts",
    "nginx.conf"
]

if not os.path.exists(BasePath):
    os.mkdir(BasePath)

for file in FileList:
    full = os.path.join(BasePath + f"/{file}")
    if not os.path.exists(full):
        with open(full, "w"):
            pass

CommandList = [
    "npm init --y",
    "npm install sequelize",
    "npm install typescript",
    "npm install express",
    "npm install nodemon",
    "npx tsc --init"
]

# for command in CommandList:
#     try:
#         result = subprocess.run(
#             command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#         if result.returncode == 0:
#             print(f"Command '{command}' executed successfully.")
#             print(result.stdout)
#         else:
#             print(f"Command '{command}' failed:")
#             print(result.stderr)

#     except Exception as e:
#         print(f"Error while executing command '{command}': {str(e)}")

src = os.path.join(BasePath+f"/src")
if not os.path.exists(src):
    os.mkdir(src)

DataFile = {
    "Db.config.ts": '''require("dotenv").config({ path: ".env" });
import { Sequelize } from 'sequelize';

const Environments = {
    preproduction: process.env.PG_CONNECTION_ALPHA,
    production: process.env.PG_CONNECTION_PRODUCTION,
    testing: process.env.PG_CONNECTION_QA,
    development: process.env.PG_CONNECTION_DEVELOPMENT,
    local: process.env.PG_CONNECTION_LOCAL,
    supertest: process.env.PG_CONNECTION_SUPERTEST
};

const Default = process.env.PG_CONNECTION_DEVELOPMENT;

const sequelize = new Sequelize(Environments[process.env.NODE_ENV] ?? Default, {
    logging: process.env.NODE_ENV.includes('local'),
    dialect: 'postgres'
});

(async () => {
    try {
        await sequelize.authenticate()
        return console.log('Database is running and ready to work.')
    } catch (error) {
        return console.log('Unable to connect database.')
    }
})();

export default sequelize;''',
    "Db.migrations.ts": '''import Db from './Db.config';

function Migrations() {
    return (async () => {
        await Db.sync({ alter: true });

        return process.exit(0)
    })();
}

export default Migrations();''',
    "Db.seeds.ts": '''// Here will be your seeds

export default (async () => {

    console.log('Seeds completed.');
    return process.exit(0)
})()'''
}

SrcList = [
    {
        "name": "Root",
        "sub": [
            "App.ts",
            "Server.ts"
        ]
    },
    {
        "name": "Api",
        "sub": [

        ]
    },
    {
        "name": "Config",
        "sub": [
            "Db.config.ts",
            "Db.migrations.ts",
            "Db.seeds.ts",
        ]
    },
    {
        "name": "Middlewares",
        "sub": [

        ]
    },
    {
        "name": "Models",
        "sub": [

        ]
    },
    {
        "name": "Scripts",
        "sub": [
            "Index.scripts.ts",
        ]
    },
    {
        "name": "Services",
        "sub": [
            "Index.services.ts",
        ]
    },
    {
        "name": "Test",
        "sub": [
            "Index.test.ts",
        ]
    },
    {
        "name": "Utils",
        "sub": [

        ]
    },
    {
        "name": "Views",
        "sub": [

        ]
    }
]

for folders in SrcList:
    if isinstance(folders, object):
        full = os.path.join(src + "/"+folders["name"])
        if not os.path.exists(full):
            if not folders["name"] == "Root":
                os.mkdir(full)
            for file in folders["sub"]:
                subfolder = os.path.join(full + f"/{file}")
                # No se llaman root
                if not folders["name"] == "Root":
                    if not os.path.exists(subfolder):
                        if file in DataFile:
                            with open(subfolder, "w") as js:
                                js.write(DataFile[file])
                        else:
                            with open(subfolder, "w"):
                                pass
                else:
                    # Se llaman root
                    subfile = os.path.join(src+"/"+file)
                    if not os.path.exists(subfile):
                        with open(subfile, "w"):
                            pass

print("Project initialized successfully.")
