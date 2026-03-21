---
name: deep-learning
description: Expert-level deep learning with PyTorch and TensorFlow. Use when building neural networks, CNNs, RNNs, transformers, training loops, loss functions, backpropagation, GPU optimization, or fine-tuning pretrained models. Also use when the user mentions 'neural network', 'PyTorch', 'transformer', 'fine-tuning', 'backpropagation', 'GPU training', 'loss function', 'overfitting', 'batch normalization', or 'transfer learning'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Deep Learning Expert

You are an expert in deep learning with deep knowledge of PyTorch, neural network architectures, training techniques, and deploying models to production.

## Before Starting

1. **Framework** — PyTorch, TensorFlow/Keras, JAX?
2. **Task type** — image classification, NLP, tabular, time-series, generative?
3. **Scale** — single GPU, multi-GPU, TPU, distributed training?
4. **Problem type** — building from scratch, fine-tuning, debugging training, deployment?
5. **Data** — how much labeled data? Any class imbalance?

---

## Core Expertise Areas

- **PyTorch fundamentals**: tensors, autograd, computational graphs, custom modules
- **Architectures**: CNN, RNN/LSTM, Transformer, attention mechanisms, ResNet
- **Training**: optimizers (Adam, AdamW, SGD), schedulers, gradient clipping
- **Regularization**: dropout, batch norm, layer norm, weight decay, early stopping
- **Transfer learning**: pretrained models, fine-tuning strategies, feature extraction
- **Hugging Face**: Transformers library, datasets, tokenizers, Trainer API
- **Performance**: mixed precision, gradient checkpointing, DataLoader optimization
- **Debugging**: loss not decreasing, NaN gradients, overfitting, underfitting

---

## Key Patterns & Code

### PyTorch Fundamentals
```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

# Device setup
device = torch.device('cuda' if torch.cuda.is_available() else
                      'mps'  if torch.backends.mps.is_available() else
                      'cpu')
print('Using device:', device)

# Tensors
x = torch.randn(32, 10, device=device)    # batch of 32, 10 features
y = torch.zeros(32, dtype=torch.long, device=device)

# Autograd
x = torch.randn(3, requires_grad=True)
y = x ** 2 + 2 * x + 1
loss = y.sum()
loss.backward()    # compute gradients
print(x.grad)      # dy/dx = 2x + 2

# No gradient for inference
with torch.no_grad():
    pred = model(x)

# Or use inference_mode (faster)
with torch.inference_mode():
    pred = model(x)
```

### Custom Neural Network Module
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class ResidualBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride=stride, padding=1, bias=False)
        self.bn1   = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1, bias=False)
        self.bn2   = nn.BatchNorm2d(out_channels)

        # Shortcut connection when dimensions change
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)  # residual connection
        return F.relu(out)


class ImageClassifier(nn.Module):
    def __init__(self, num_classes: int = 10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2, padding=1),
            ResidualBlock(64, 64),
            ResidualBlock(64, 128, stride=2),
            ResidualBlock(128, 256, stride=2),
        )
        self.pool       = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.pool(x)
        return self.classifier(x)

model = ImageClassifier(num_classes=10).to(device)
print('Parameters:', sum(p.numel() for p in model.parameters() if p.requires_grad))
```

### Production Training Loop
```python
import torch
import torch.nn as nn
from torch.cuda.amp import GradScaler, autocast
from torch.utils.data import DataLoader
from tqdm import tqdm
import wandb

def train_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    scaler: GradScaler,
    device: torch.device,
    grad_clip: float = 1.0,
) -> dict:
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (inputs, targets) in enumerate(tqdm(loader, desc='Train')):
        inputs  = inputs.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)  # faster than zero_grad()

        # Mixed precision forward pass
        with autocast(device_type='cuda', dtype=torch.float16):
            outputs = model(inputs)
            loss    = criterion(outputs, targets)

        # Scaled backward pass
        scaler.scale(loss).backward()

        # Gradient clipping (prevents exploding gradients)
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)

        scaler.step(optimizer)
        scaler.update()

        # Metrics
        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total   += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    return {
        'loss':     total_loss / len(loader),
        'accuracy': correct / total,
    }

@torch.no_grad()
def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict:
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0

    for inputs, targets in tqdm(loader, desc='Eval'):
        inputs  = inputs.to(device, non_blocking=True)
        targets = targets.to(device, non_blocking=True)

        with autocast(device_type='cuda', dtype=torch.float16):
            outputs = model(inputs)
            loss    = criterion(outputs, targets)

        total_loss += loss.item()
        _, predicted = outputs.max(1)
        total   += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    return {
        'loss':     total_loss / len(loader),
        'accuracy': correct / total,
    }


def train(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    num_epochs: int = 50,
    lr: float = 1e-3,
    weight_decay: float = 1e-4,
):
    model = model.to(device)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)
    scaler    = GradScaler()

    best_val_acc = 0.0
    patience = 0
    max_patience = 10  # early stopping

    for epoch in range(num_epochs):
        train_metrics = train_epoch(model, train_loader, optimizer, criterion, scaler, device)
        val_metrics   = evaluate(model, val_loader, criterion, device)
        scheduler.step()

        print(
            f'Epoch {epoch+1}/{num_epochs} | '
            f'Train Loss: {train_metrics["loss"]:.4f} Acc: {train_metrics["accuracy"]:.4f} | '
            f'Val Loss: {val_metrics["loss"]:.4f} Acc: {val_metrics["accuracy"]:.4f}'
        )

        wandb.log({'epoch': epoch, **train_metrics, **{'val_' + k: v for k, v in val_metrics.items()}})

        # Save best model
        if val_metrics['accuracy'] > best_val_acc:
            best_val_acc = val_metrics['accuracy']
            torch.save({'epoch': epoch, 'model_state_dict': model.state_dict(),
                        'optimizer_state_dict': optimizer.state_dict(),
                        'val_accuracy': best_val_acc}, 'best_model.pt')
            patience = 0
        else:
            patience += 1
            if patience >= max_patience:
                print('Early stopping at epoch', epoch + 1)
                break

    return best_val_acc
```

### Transfer Learning with Hugging Face
```python
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)
from datasets import load_dataset, Dataset
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
import torch

# Load pretrained model and tokenizer
MODEL_NAME = 'distilbert-base-uncased'
NUM_LABELS = 2

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model     = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=NUM_LABELS,
)

# Tokenize dataset
def tokenize(examples):
    return tokenizer(
        examples['text'],
        truncation=True,
        max_length=512,
        padding=False,   # DataCollator handles padding
    )

dataset = load_dataset('imdb')
tokenized = dataset.map(tokenize, batched=True, remove_columns=['text'])
tokenized = tokenized.rename_column('label', 'labels')

# Metrics
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        'accuracy': accuracy_score(labels, predictions),
        'f1':       f1_score(labels, predictions, average='weighted'),
    }

# Training arguments
args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_ratio=0.1,
    evaluation_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    metric_for_best_model='f1',
    fp16=torch.cuda.is_available(),
    logging_steps=100,
    report_to='wandb',
    dataloader_num_workers=4,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized['train'],
    eval_dataset=tokenized['test'],
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer),
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.evaluate()
trainer.save_model('./final_model')
```

### Fine-tuning Strategies
```python
from transformers import AutoModelForSequenceClassification
import torch.nn as nn

model = AutoModelForSequenceClassification.from_pretrained('bert-base-uncased')

# Strategy 1: Feature extraction — freeze all, train only classifier head
for param in model.base_model.parameters():
    param.requires_grad = False
# Only classifier head is trainable
# Use when: very little data, fast training needed

# Strategy 2: Fine-tune last N layers only
for name, param in model.named_parameters():
    param.requires_grad = False

# Unfreeze last 2 transformer layers + classifier
for name, param in model.named_parameters():
    if any(layer in name for layer in ['layer.10', 'layer.11', 'classifier']):
        param.requires_grad = True
# Use when: moderate data, balance speed and performance

# Strategy 3: Full fine-tuning with discriminative learning rates
# Lower LR for earlier layers, higher LR for later layers
optimizer_groups = [
    {'params': model.bert.embeddings.parameters(), 'lr': 1e-5},
    {'params': model.bert.encoder.layer[:6].parameters(), 'lr': 2e-5},
    {'params': model.bert.encoder.layer[6:].parameters(), 'lr': 3e-5},
    {'params': model.classifier.parameters(), 'lr': 5e-5},
]
optimizer = torch.optim.AdamW(optimizer_groups, weight_decay=0.01)
# Use when: sufficient data, best performance needed

# Strategy 4: LoRA (Low-Rank Adaptation) — memory efficient fine-tuning
from peft import get_peft_model, LoraConfig, TaskType

lora_config = LoraConfig(
    task_type=TaskType.SEQ_CLS,
    r=8,                  # rank of low-rank matrices
    lora_alpha=32,        # scaling factor
    lora_dropout=0.1,
    target_modules=['query', 'value'],  # which layers to adapt
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Trainable: 0.3% of parameters — 10x less memory!
```

### Custom Dataset
```python
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import pandas as pd
import os

class ImageDataset(Dataset):
    def __init__(self, csv_path: str, img_dir: str, transform=None, augment=None):
        self.df        = pd.read_csv(csv_path)
        self.img_dir   = img_dir
        self.transform = transform
        self.augment   = augment

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int):
        row      = self.df.iloc[idx]
        img_path = os.path.join(self.img_dir, row['filename'])
        image    = Image.open(img_path).convert('RGB')
        label    = row['label']

        if self.augment:
            image = self.augment(image)
        if self.transform:
            image = self.transform(image)

        return image, label

# Transforms
train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# DataLoaders
train_dataset = ImageDataset('train.csv', 'images/', transform=train_transform)
val_dataset   = ImageDataset('val.csv',   'images/', transform=val_transform)

train_loader = DataLoader(
    train_dataset,
    batch_size=64,
    shuffle=True,
    num_workers=4,
    pin_memory=True,    # faster GPU transfer
    persistent_workers=True,  # keep workers alive between epochs
    prefetch_factor=2,
)
```

### Debugging Training Issues
```python
# Issue 1: Loss is NaN
# Causes: exploding gradients, bad learning rate, NaN in data
# Fix:
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)  # lower LR
# Check data:
assert not torch.isnan(inputs).any(), 'NaN in inputs'
assert not torch.isinf(inputs).any(), 'Inf in inputs'

# Issue 2: Loss not decreasing
# Check 1: Can model overfit a single batch?
model.train()
for _ in range(100):
    loss = criterion(model(single_batch_x), single_batch_y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    print(loss.item())  # should decrease to near 0

# Issue 3: Overfitting
# Solutions:
model = nn.Sequential(
    ...,
    nn.Dropout(0.3),      # add dropout
    nn.BatchNorm1d(256),  # add batch norm
    ...
)
optimizer = torch.optim.AdamW(model.parameters(), weight_decay=1e-2)  # L2 reg
criterion = nn.CrossEntropyLoss(label_smoothing=0.1)  # label smoothing

# Issue 4: GPU memory error
# Fix: reduce batch size or use gradient checkpointing
from torch.utils.checkpoint import checkpoint

class MemoryEfficientModel(nn.Module):
    def forward(self, x):
        # Recompute activations during backward pass to save memory
        return checkpoint(self.expensive_block, x, use_reentrant=False)

# Monitor GPU memory
print(torch.cuda.memory_allocated() / 1024**2, 'MB allocated')
print(torch.cuda.memory_reserved()  / 1024**2, 'MB reserved')
torch.cuda.empty_cache()  # free cached memory
```

### Model Export for Inference
```python
import torch
import torch.onnx

model.eval()

# Export to TorchScript (for C++ deployment)
scripted = torch.jit.script(model)
scripted.save('model_scripted.pt')

# Export to ONNX (for cross-platform deployment)
dummy_input = torch.randn(1, 3, 224, 224, device=device)
torch.onnx.export(
    model,
    dummy_input,
    'model.onnx',
    export_params=True,
    opset_version=17,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input':  {0: 'batch_size'},
        'output': {0: 'batch_size'},
    },
)

# Verify ONNX model
import onnx, onnxruntime
onnx.checker.check_model('model.onnx')

session = onnxruntime.InferenceSession('model.onnx')
outputs = session.run(None, {'input': dummy_input.cpu().numpy()})
```

---

## Best Practices

- Always check if model can overfit a single batch before training on full dataset
- Use mixed precision (float16/bfloat16) — 2x speedup, 2x memory reduction
- Set num_workers > 0 in DataLoader and pin_memory=True for GPU training
- Use gradient clipping to prevent exploding gradients (max_norm=1.0)
- Log training curves — loss, accuracy, learning rate — with wandb or TensorBoard
- Save checkpoints regularly — never lose hours of training to a crash
- Use label smoothing for classification — improves generalization
- Validate that val set is never seen during training — no leakage

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| model.train() forgotten | Dropout and BatchNorm behave differently | Always set model.train() for training |
| No model.eval() at inference | Wrong predictions due to dropout | Always set model.eval() for evaluation |
| optimizer.zero_grad() missing | Gradients accumulate across batches | Call zero_grad() before each backward |
| Loss on GPU, metrics on CPU | Slow transfers every step | Keep metrics computation on GPU |
| DataLoader num_workers=0 | CPU bottleneck starves GPU | Set num_workers to 4-8 |
| No gradient clipping | NaN loss from exploding gradients | Add clip_grad_norm_ before optimizer.step() |
| Same transforms for train/val | Data leakage or wrong evaluation | Use augmentation only for train split |
| Not normalizing inputs | Slow convergence, instability | Normalize with dataset mean/std |

---

## Related Skills

- **machine-learning**: For traditional ML alongside deep learning
- **llm-engineering**: For LLM-powered applications
- **mlops-expert**: For deploying and monitoring deep learning models
- **python-expert**: For Python performance optimization
- **data-engineering**: For building data pipelines for training data
- **docker-expert**: For containerizing training and inference