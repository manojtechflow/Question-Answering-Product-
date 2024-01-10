from haystack.nodes import FARMReader

# Load the pretrained BERT SQuAD 2.0 model
model_name = r"C:\Users\thota\Desktop\Project\HS\Digitization\Models\Roberta_distill"
reader = FARMReader(model_name_or_path=model_name, use_gpu=True)
data_dir = r"C:\Users\thota\Desktop\Project\HS\Digitization\data_set"
# data_dir = "PATH/TO_YOUR/TRAIN_DATA"
reader.train(data_dir=data_dir, train_filename="custom_train_data.json", use_gpu=True, n_epochs=10, save_dir=r"C:\Users\thota\Desktop\Project\HS\Digitization\Models\trained_roberta")

# Saving the model happens automatically at the end of training into the `save_dir` you specified
# However, you could also save a reader manually again via:
reader.save(directory=r"C:\Users\thota\Desktop\Project\HS\Digitization\Models\trained_roberta")
