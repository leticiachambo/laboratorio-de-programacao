"""
DogVision — Preparação do conjunto de dados
=============================================

Este script converte as anotações do Stanford Dogs Dataset (formato
Pascal VOC / XML) para o formato utilizado no treinamento do modelo de
detecção de objetos na Unidade 2 (YOLO: classe + coordenadas normalizadas),
e particiona o conjunto resultante em treino, validação e teste, de forma
estratificada por classe (raça).

Estrutura esperada de entrada (após baixar e extrair o Stanford Dogs Dataset,
ver dataset/README.md para instruções de download):

    dataset/raw/
        Images/
            n02085620-Chihuahua/*.jpg
            n02085782-Japanese_spaniel/*.jpg
            ...
        Annotation/
            n02085620-Chihuahua/*           (arquivos XML sem extensão, Pascal VOC)
            n02085782-Japanese_spaniel/*
            ...

Estrutura gerada em dataset/processed/:

    dataset/processed/
        train/images/*.jpg   train/labels/*.txt
        val/images/*.jpg     val/labels/*.txt
        test/images/*.jpg    test/labels/*.txt
        classes.txt          (uma classe por linha, na ordem usada nos rótulos)
        raca_seed.csv        (dados prontos para popular a tabela `raca`)

Uso:
    python prepare_dataset.py --raças Chihuahua Beagle Pug ... \
                               --train 0.70 --val 0.15 --test 0.15

Se --racas não for informado, o script usa uma lista padrão de 12 raças
com quantidade equilibrada de imagens (ver DEFAULT_BREEDS abaixo).

Dependências: pip install -r ../requirements.txt
"""

import argparse
import csv
import random
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

RAW_DIR = Path(__file__).parent / "raw"
IMAGES_DIR = RAW_DIR / "Images" / "Images"
ANNOTATION_DIR = RAW_DIR / "Annotation" / "Annotation"
OUT_DIR = Path(__file__).parent / "processed"

# Subconjunto padrão de raças (ajustar conforme escolha da equipe).
# O nome deve corresponder ao sufixo da pasta no dataset original,
# ex.: pasta "n02085620-Chihuahua" -> "Chihuahua".
DEFAULT_BREEDS = [
    "Chihuahua", "Japanese_spaniel", "Maltese_dog", "Pekinese",
    "Beagle", "Basset", "Bloodhound", "Pug", "Rottweiler",
    "German_shepherd", "Golden_retriever", "Labrador_retriever",
]


def find_breed_dir(base_dir: Path, breed: str) -> Path:
    breed_lower = breed.lower()

    matches = [
        p for p in base_dir.iterdir()
        if p.is_dir() and p.name.lower().endswith(breed_lower)
    ]

    if not matches:
        raise FileNotFoundError(
            f"Raça '{breed}' não encontrada em {base_dir}"
        )

    return matches[0]


def parse_voc_annotation(xml_path: Path):
    """Lê um arquivo Pascal VOC e retorna (largura, altura, [(xmin,ymin,xmax,ymax), ...])."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)
    boxes = []
    for obj in root.findall("object"):
        bnd = obj.find("bndbox")
        xmin, ymin = int(bnd.find("xmin").text), int(bnd.find("ymin").text)
        xmax, ymax = int(bnd.find("xmax").text), int(bnd.find("ymax").text)
        boxes.append((xmin, ymin, xmax, ymax))
    return width, height, boxes


def voc_to_yolo_line(class_id, width, height, box):
    xmin, ymin, xmax, ymax = box
    x_center = ((xmin + xmax) / 2) / width
    y_center = ((ymin + ymax) / 2) / height
    box_w = (xmax - xmin) / width
    box_h = (ymax - ymin) / height
    return f"{class_id} {x_center:.6f} {y_center:.6f} {box_w:.6f} {box_h:.6f}"


def collect_samples(breeds):
    """Retorna lista de (imagem_path, anotacao_path, class_id, class_name)."""
    samples = []
    for class_id, breed in enumerate(breeds):
        img_dir = find_breed_dir(IMAGES_DIR, breed)
        ann_dir = find_breed_dir(ANNOTATION_DIR, breed)
        for img_path in sorted(img_dir.glob("*.jpg")):
            ann_path = ann_dir / img_path.stem  # arquivos de anotação não têm extensão
            if ann_path.exists():
                samples.append((img_path, ann_path, class_id, img_dir.name))
    return samples


def stratified_split(samples, train_ratio, val_ratio, test_ratio, seed=42):
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
        "As proporções de treino, validação e teste devem somar 1.0"

    by_class = {}
    for s in samples:
        by_class.setdefault(s[2], []).append(s)

    rng = random.Random(seed)
    train, val, test = [], [], []
    for class_id, items in by_class.items():
        rng.shuffle(items)
        n = len(items)
        n_train = int(n * train_ratio)
        n_val = int(n * val_ratio)
        train += items[:n_train]
        val += items[n_train:n_train + n_val]
        test += items[n_train + n_val:]
    return train, val, test


def write_split(name, samples, breeds):
    img_out = OUT_DIR / name / "images"
    lbl_out = OUT_DIR / name / "labels"
    img_out.mkdir(parents=True, exist_ok=True)
    lbl_out.mkdir(parents=True, exist_ok=True)

    for img_path, ann_path, class_id, _ in samples:
        width, height, boxes = parse_voc_annotation(ann_path)
        shutil.copy(img_path, img_out / img_path.name)
        lines = [voc_to_yolo_line(class_id, width, height, b) for b in boxes]
        (lbl_out / (img_path.stem + ".txt")).write_text("\n".join(lines))

    print(f"[{name}] {len(samples)} imagens gravadas em {img_out}")


def write_metadata(breeds):
    (OUT_DIR / "classes.txt").write_text("\n".join(breeds))

    with open(OUT_DIR / "raca_seed.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["nome_popular", "nome_cientifico", "origem_dataset"])
        for breed in breeds:
            breed_dir = find_breed_dir(IMAGES_DIR, breed)
            writer.writerow([breed.replace("_", " "), "", breed_dir.name])
    print(f"Metadados gravados em {OUT_DIR}/classes.txt e {OUT_DIR}/raca_seed.csv")


def main():
    parser = argparse.ArgumentParser(description="Prepara (anota/converte e particiona) o dataset DogVision")
    parser.add_argument("--racas", nargs="+", default=DEFAULT_BREEDS, help="Lista de raças a incluir")
    parser.add_argument("--train", type=float, default=0.70)
    parser.add_argument("--val", type=float, default=0.15)
    parser.add_argument("--test", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if not IMAGES_DIR.exists() or not ANNOTATION_DIR.exists():
        raise SystemExit(
            "Dataset bruto não encontrado. Baixe e extraia o Stanford Dogs Dataset em "
            f"'{RAW_DIR}' conforme as instruções em dataset/README.md antes de executar este script."
        )

    print(f"Coletando amostras para {len(args.racas)} raças...")
    samples = collect_samples(args.racas)
    print(f"Total de amostras coletadas: {len(samples)}")

    train, val, test = stratified_split(samples, args.train, args.val, args.test, seed=args.seed)

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)

    write_split("train", train, args.racas)
    write_split("val", val, args.racas)
    write_split("test", test, args.racas)
    write_metadata(args.racas)

    print("\nResumo do particionamento:")
    print(f"  Treino:     {len(train)} imagens")
    print(f"  Validação:  {len(val)} imagens")
    print(f"  Teste:      {len(test)} imagens")
    print(f"  Total:      {len(train) + len(val) + len(test)} imagens")


if __name__ == "__main__":
    main()
