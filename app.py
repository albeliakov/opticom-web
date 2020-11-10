from flask import Flask, render_template
import os
import json
from pprint import pprint

app = Flask(__name__)
app_dir = os.path.dirname(os.path.abspath(__file__))


#######################################################
# HELPER FUNCTIONS
#######################################################


def safe_list_dir(path):
    """Сохраняет список файлов и директорий в указанной папке."""
    print(path)
    try:
        return [x for x in os.listdir(path) if not x.startswith(".")]
    except:
        return []


#######################################################
# OTHER FUNCTION
#######################################################


@app.route("/")
def root():
    """
    Главная страница с возможностями: запуска нового расчета и просмотра
    ранее полученных результатов.
    """

    user = "admin"
    user_is_admin = user == "admin"
    if user_is_admin:  # Для админа выводятся все посчитанные модели.
        all_models = [{"owner": owner, "name": mod}
                      for owner in safe_list_dir("data/Model/")
                      for mod in safe_list_dir("data/Model/" + owner)]
    else:  # Для пользователя выбираются только доступные модели.
        public_models = [{"owner": "public", "name": x} for x in
                         safe_list_dir("data/Model/public/")]
        user_models = [{"owner": user, "name": x} for x in
                       safe_list_dir("data/Model/" + user)]
        all_models = public_models + user_models
    # pprint(all_models)
    for mod in all_models:  # Дополнить выбранные модели мета-данными.
        model_path = os.path.join(app_dir, "data", "Model", mod["owner"],
                                  mod["name"], "inputData.json")
        print(model_path)
        with open(model_path, 'r', encoding='utf-8') as f:
            model_input_data = json.load(f)
        mod["modelType"] = model_input_data["modelType"]
        mod["simStartDate"] = model_input_data["simStartDate"]
        # mod["companyName"] = model_input_data["companyName"]
        # mod["owner"] = model_input_data["companyName"]
    # pprint(all_models)
    model_types_path = os.path.join(app_dir, "opticom", "models",
                                    "model_types.json")
    with open(model_types_path, 'r', encoding='utf-8') as f:
        model_names = json.load(f)["listModelType"]
    return render_template("my_home.html", models=all_models, current_user="admin",
                           is_admin=user_is_admin, modelNames=model_names,
                           modelTips={})

if __name__ == "__main__":
    app.run(port=8000)
    # root()