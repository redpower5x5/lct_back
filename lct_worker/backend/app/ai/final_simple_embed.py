import torch
import torchvision
import pickle
import os

model = torch.load('model.pt')
model.eval()

THRESHOLD = 0.6
def is_spotted_before(embed, mean_embeds_path):
    for file in os.listdir(mean_embeds_path):
        with open(os.path.join(mean_embeds_path, file), 'rb') as f:
            mean_embed = embed
        if torch.nn.CosineSimilarity()(embed, mean_embed).item() > THRESHOLD:
            return 1
    return 0

def add_new_member(frames_paths, task_id):
    mean_embed = torch.zeros()
    for file in os.listdir(frames_paths):
        image = torchvision.io.read_image(f'{frames_paths}/{file}')
        if image.shape[1] < 80:
            image = torchvision.transforms.functional.pad(image, (0, (80 - image.shape[1])//2 + 1))
        if image.shape[2] < 80:
            image = torchvision.transforms.functional.pad(image, ((80 - image.shape[2])//2 + 1), 0)
        mean_embed = model((image / 255).unsqueeze(dim = 0))
    mean_embed /= len(frames_paths)
    with open(f'{mean_embeds_path}/{task_id}.pickle', 'wb') as f:
        pickle.dump(mean_embed, f)


def get_embed(frame_path):
    image = torchvision.io.read_image(frame_path)
    if image.shape[1] < 80:
        image = torchvision.transforms.functional.pad(image, (0, (80 - image.shape[1])//2 + 1))
    if image.shape[2] < 80:
        image = torchvision.transforms.functional.pad(image, ((80 - image.shape[2])//2 + 1), 0)
    embed = model((image / 255).unsqueeze(dim = 0))
    return embed