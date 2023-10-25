from logging import exception
from statistics import mode
import sys
import os
import subprocess

BasePath = "structure"
src_models = os.path.join(BasePath+f"/src/Models")
src_config = os.path.join(BasePath+f"/src/Config")

if not os.path.exists(src_models) or not os.path.exists(src_config):
    print("Please, make sure to init a project before to make a model.")
    exit()

models = os.listdir(src_models)
total_models = len(models)


def model(model, id):
    capitalize = model.capitalize()
    return f'''import {{Model, DataTypes, InferAttributes, InferCreationAttributes, ForeignKey}} from 'sequelize';
import Database from '../Config/Db.config';

export interface I{capitalize} {{

}}

class {capitalize} extends Model<InferAttributes<{capitalize}>, InferCreationAttributes<{capitalize}>>{{

}};

{capitalize}.init(
    {{

    }},
    {{
        tableName: '{capitalize}',
        indexes: [
            {{
                unique: true,
                fields: ['{id}']
            }}
        ],
        createdAt: "CreatedAt", // alias createdAt as tCreatedAt
        updatedAt: "UpdatedAt", // alias updatedAt as tUpdatedAt
        sequelize: Database, // passing the `sequelize` instance is required
    }},
);

export default {capitalize};
'''


if len(sys.argv) > 2:
    file = sys.argv[1]
    id = sys.argv[2]

    if f"{file}.models.ts" in models:
        print("Please make sure to write a model that is not included in model's folder.")
        exit()

    with open(src_models+f"/{file.capitalize()}.models.ts", "w") as js:
        js.write(model(file, id))
    full = f"{src_config}/Db.migrations.ts"
    with open(full, "r") as js:
        lines = js.readlines()

    import_number = 1 + total_models
    migration_number = 5 + total_models

    lines[import_number-1] += f'import {file} from "../Models/{file}.models";' +'\n'
    lines[migration_number-1] += f"\t\tconsole.log('{file}', {file} == Db.models.{file});" +'\n'

    with open(full, "w") as js:
        js.write(''.join(lines))

    print(f"Model {file} successfully created.")

else:
    print("Method required 2 params (model_name, id_name)")
