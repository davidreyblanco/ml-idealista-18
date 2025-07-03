
import wandb
import joblib
import os    
import pandas as pd


def get_wandb_model(project_name, target_configuration, debug=False):

    """
    Retrieves a specific model from Weights & Biases based on the project and configuration.
    """
    api = wandb.Api()
    type_name = 'model'  # The type of artifact we are looking for
    
    collections = api.artifact_collections(project_name = project_name, type_name = type_name)

    target_artifact = None
    # Get the list of collections
    for collection in collections:
        if debug:
            print(f"📁 Collection: {collection.name} - Project: {project_name}")
        
        # Now iterate over artifacts in the collection
        for artifact in collection.artifacts():
            if debug:
                print(f"  🔹 Artifact: {artifact.name} - Version: {artifact.version}")
                print(f"  🔹 Tags: {artifact.metadata['tags']}")
            if target_configuration in artifact.metadata['tags']:
                artifact_dir = artifact.download()
                files = os.listdir(artifact_dir)
                model_filename = files[0]  
                target_artifact = joblib.load(os.path.join(artifact_dir, model_filename))

                if debug:
                    print(f"  🔸 Found Target configuration found: {target_configuration}")
                break
    
    return target_artifact

def get_dataset(artifact_name, project_name, debug=False):
    """
    Retrieves a dataset artifact from Weights & Biases.
    """
    type_name = 'dataset'
    X_train, X_test, y_train, y_test = None, None, None, None
    
    # Download the dataset splits artifact from W&B
    with wandb.init(project=project_name) as run:
        artifact = run.use_artifact(artifact_name, type=type_name)
        artifact_dir = artifact.download()

        # Load the splits from the artifact directory
        X_train = pd.read_csv(f"{artifact_dir}/X_train.csv.gz", compression='gzip')
        X_test = pd.read_csv(f"{artifact_dir}/X_test.csv.gz", compression='gzip')
        y_train = pd.read_csv(f"{artifact_dir}/y_train.csv.gz", compression='gzip').squeeze()
        y_test = pd.read_csv(f"{artifact_dir}/y_test.csv.gz", compression='gzip').squeeze()

        if debug:
            print("------------------------------------------")
            print("Loaded splits from W&B artifact:")
            print("------------------------------------------")

            print("X_train shape:", X_train.shape)
            print("X_test shape:", X_test.shape)
            print("y_train shape:", y_train.shape)
            print("y_test shape:", y_test.shape)
    
    return X_train, X_test, y_train, y_test